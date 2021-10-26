from PIL import Image, ImageDraw, ImageFont

def test_demotivator():
    first_text = "абобус"
    second_text = "да"
    photo = "photo_test.png"

    # Создание демотиватора
    original = Image.open("Demotivator.png").convert('RGB')
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
    original = original.save("DemotivatorFinal.png")
