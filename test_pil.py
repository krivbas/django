from PIL import Image, ImageDraw, ImageFont


im = Image.open('cage.jpg')


# (left, upper, right, lower)
# box = (100, 50, 400, 200)

# im = im.crop(box)
# im = im.resize((128, 128))

# im = im.rotate(45)
draw = ImageDraw.Draw(im)
font_montserrat_28 = ImageFont.truetype("Montserrat-SemiBold.otf", 28)
text = 'CAGE cage CAGE'
cage_color = "#4a4a4a"
cage_position = (0, 0)
draw.text(cage_position, text, fill=cage_color, font=font_montserrat_28)


im.save('cage2.jpg')
# im.show()