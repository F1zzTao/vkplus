from PIL import Image, ImageDraw, ImageFont

def test_demotivator():
    first_text = "абобус"
    second_text = "да"
    photo = "tests/dem_generator/photo_test.png"
    original = "tests/dem_generator/Demotivator.png"

    # Создание демотиватора
    original = Image.open(original).convert('RGB')
    to_paste = Image.open(photo).convert('RGB')
    fnt = ImageFont.truetype("TNR.ttf", 70)
    fnt1 = ImageFont.truetype("TNR.ttf", 40)
    d = ImageDraw.Draw(original)
    d_paste = ImageDraw.Draw(to_paste)

    original.paste(to_paste.resize((609, 517)), (75, 45))

    w, h = original.size
    W, H = d.textsize(first_text, font=fnt)
    W1, H1 = d.textsize(second_text, font=fnt1)

    d.text(((w-W)/2, 575), first_text, font=fnt, fill="white")
    d.text(((w-W1)/2, 650), second_text, font=fnt1, fill="white")
    original = original.save("tests/dem_generator/DemotivatorFinal.png")
