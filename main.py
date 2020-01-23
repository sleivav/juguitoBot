from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram import ParseMode

from io import BytesIO


def generate_image(text_array, font):
    img = Image.open('resources/base.jpg')
    draw = ImageDraw.Draw(img)
    text = Image.new('RGBA', (176 * 4, 62 * 4), (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text)
    text_draw.text((0, 0), text_array[0] + "\n" + text_array[1], font=font, fill=(25, 25, 25))
    paste = text.rotate(1.5).resize((176, 62), Image.ANTIALIAS)

    img.paste(paste, (354, 525), paste)
    #img.save('sample-out.jpg', quality=100)
    return img


def split_text(juice_text):
    width = font.getsize(juice_text)[0] / 4
    if width > 176 * 2:
        return [False, juice_text, "", 0]
    elif width < 176:
        return [True, juice_text, ""]
    else:
        words = juice_text.split()
        first_line = ""
        index = 0
        while font.getsize(first_line + words[index])[0] / 4 < 176:
            first_line += words[index] + " "
            index += 1
        second_line = " ".join(word for word in words[index:])
        if font.getsize(second_line)[0] / 4 > 176:
            return [False, first_line, second_line, 2]
        return [True, first_line, second_line]


def get_image_bio(img):
    bio = BytesIO()
    bio.name = 'image.jpeg'
    img.save(bio, 'JPEG', quality=100)
    bio.seek(0)
    return bio


def send_error_message(update, context, param):
    if param[2] == 0:
        message = "El largo total de tu texto es muy largo para intentar separarlo uwu"
    else:
        message = "Intenté separar el texto en *" + param[0] + "*y *" + param[1] +\
                  "*, pero la segunda línea quedó muy larga y no pude mandarlo uwu"
    context.bot.send_photo(chat_id=update.message.chat_id, photo=open('resources/muy_largo_uwu.jpg', 'rb'),
                           caption=message, parse_mode=ParseMode.MARKDOWN)


def send_juguito(update, context):
    args = context.args
    if (len(context.args)) < 1:
        return
    if update.message.text.split()[0] == "/juguitoDe":
        args.insert(0, "de")
        args.insert(0, "juguito")
    text = ' '.join(args)
    text_split = split_text(text)
    if not text_split[0]:
        return send_error_message(update, context, text_split[1:])
    img = generate_image(text_split[1:], font)
    bio = get_image_bio(img)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=bio)


if __name__ == '__main__':
    font = ImageFont.truetype('resources/HindJalandhar-Regular.ttf', 24 * 4)
    updater = Updater(token='token', use_context=True)
    dispatcher = updater.dispatcher
    juguito_handler = CommandHandler('juguito', send_juguito)
    juguito_de_handler = CommandHandler('juguitoDe', send_juguito)
    dispatcher.add_handler(juguito_handler)
    dispatcher.add_handler(juguito_de_handler)
    updater.start_polling()
