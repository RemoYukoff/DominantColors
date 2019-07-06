import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PIL import Image, ImageDraw
from sklearn.cluster import KMeans
import numpy as np


class DominantColors():
    CLUSTERS = None
    IMAGE = None
    LABELS = None
    COLORS = None

    def __init__(self, image, clusters=3):
        self.IMAGE = image
        self.CLUSTERS = clusters

    def get_colors(self):
        # Resize for optimization
        img = Image.open(self.IMAGE).resize((200,200))
        img = np.array(img.getdata())

        self.IMAGE = img
        kmean = KMeans(n_clusters=self.CLUSTERS)
        kmean.fit(img)

        # Save color in hex format
        to_hex = lambda rgb: "#{:02x}{:02x}{:02x}".format(*rgb)
        self.COLORS = kmean.cluster_centers_.astype(int)
        self.COLORS = np.apply_along_axis(to_hex, 1, self.COLORS)

        self.LABELS = kmean.labels_

        return self.COLORS
    
    def color_frequency(self):
        # Generate data
        hist, _ = np.histogram(self.LABELS,self.CLUSTERS)

        frequencies = hist/hist.sum()
        sort_order = np.argsort(frequencies)[::-1]

        # Sort biggest to smaller
        colors = self.COLORS[sort_order]
        frequencies = frequencies[sort_order]

        # Create Image
        width, height = (500,250)
        img = Image.new("RGB",(width,height))
        draw = ImageDraw.Draw(img, "RGB")

        # Draw
        start = 0
        for color, frequency in zip(colors, frequencies):
            end = start+frequency*width
            draw.rectangle([start,0,end,height], fill=color)
            start = end
        
        # Save
        img.save("color_frequency.png")

    def show_plot(self):
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.scatter(self.IMAGE[:, 0],self.IMAGE[:, 1],self.IMAGE[:, 2], c=self.COLORS[self.LABELS])
        plt.show()
