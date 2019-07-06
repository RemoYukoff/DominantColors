from dominantcolors import DominantColors


image_path = "test.jpg"

dc = DominantColors(image_path,4)

colors = dc.get_colors()
print(colors)

dc.color_frequency()
dc.show_plot()
