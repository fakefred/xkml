from PIL import Image, ImageDraw, ImageFont


def drawText(canvas: Image, text: str, position: tuple, size=20,
             color='black', uppercase=True, maxwidth=0, center=0) -> tuple:
    xkcd_script = ImageFont.truetype('./xkcd_script.ttf', size)
    draw = ImageDraw.Draw(canvas)
    if uppercase:
        text = text.upper()
    # maxwidth: set to 0 to disable textwrap
    wrapped_text = wrapText(
        text, maxwidth, xkcd_script) if maxwidth != 0 else text
    # center: set to 0 to disable center
    # TODO: center text around `center` axis
    # text_width = draw.multiline_textsize(wrapped_text, font=xkcd_script)

    draw.multiline_text(position, wrapped_text, fill=color, font=xkcd_script)
    return draw.multiline_textsize(wrapped_text, font=xkcd_script)


def wrapText(text: str, maxwidth: int, font) -> str:
    # maxwidth: in pixels
    # wraps text in terms of graphical width displayed in font xkcd_script
    # TODO: hyphenation

    # initiate drawing context
    canvas = Image.new('RGB', (1, 1), color=(255, 255, 255))
    draw = ImageDraw.Draw(canvas)

    # split words and iterate
    words = text.split(' ')
    current_line = ''
    wrapped_text = ''
    for word in words:
        line_width = draw.textsize(current_line + word, font=font)[0]
        if line_width <= maxwidth:
            # append word
            current_line += word + ' '
            wrapped_text += word + ' '
        else:
            # linebreak
            wrapped_text += '\n' + word + ' '
            # reset buffer
            current_line = word + ' '

    return wrapped_text
