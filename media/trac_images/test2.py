import Image
im = Image.new("RGB", (100, 100))
import ImageDraw
draw = ImageDraw.Draw(im)
draw.text((50, 50), "hey")
im.rotate(45).show()

