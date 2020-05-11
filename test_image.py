from PIL import Image, ImageDraw, ImageFont

img = Image.new('1', (40, 40), 1)
draw = ImageDraw.Draw(img)

draw.rectangle(((5, 5), (35, 35)))
draw.ellipse((0, 0, 11, 11), fill='white', outline='black')
draw.ellipse((0, 29, 11, 40), fill='white', outline='black')
draw.ellipse((29, 29, 40, 40), fill='white', outline='black')
draw.ellipse((29, 0, 40, 11), fill='white', outline='black')

font = font = ImageFont.truetype('/usr/share/fonts/liberation/LiberationMono-Regular.ttf', 18)
draw.text((14, 11), '4', fill='black', font=font)

img.save('test_image.png')

