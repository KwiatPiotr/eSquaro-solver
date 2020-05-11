from PIL import Image, ImageDraw, ImageFont
from  puzzles import grid_3_3

grid = [
	[1, 2, 3, 4],
	[3, 4, 0, 3],
	[3, 2, 1, 2],
	[1, 1, 1, 1]
]

x_len = len(grid)
y_len = len(grid[0])

print(x_len, y_len)

img = Image.new('1', (40*x_len, 40*y_len), 1)
draw = ImageDraw.Draw(img)
font = font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationMono-Regular.ttf', 18)

for i in range(x_len):
	for j in range(y_len):
		beg = (30 * i + 5, 30 * j + 5)
		end = (30 * i + 35, 30 * j + 35)
		text_pnt = (30 * i + 14, 30 * j + 11)
		draw.rectangle((beg, end))
		draw.text(text_pnt, str(grid[i][j]), fill='black', font=font)

for i in range(x_len + 1):
	for j in range(y_len + 1):
		if (i + j) % 2 == 1:
			draw.ellipse((i * 30, j * 30, i * 30 + 11, j * 30 + 11), fill='white', outline='black')
		else:
			draw.ellipse((i * 30, j * 30, i * 30 + 11, j * 30 + 11), fill='black', outline='black')

img.save('test_image_grid.png')

