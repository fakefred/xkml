from PIL import Image, ImageDraw
from drawfigure import drawFigure, paste
from drawdialogs import drawDialogs


def drawPanel(canvas: Image, dimensions: tuple, figures: dict, dialogs: dict, cast: dict):
    # figures: dict of figure data
    # {
    #   'cueball': {
    #       'ims': ims_dict,
    #       'params': params_dict
    #   },
    #   'megan': {...},
    #   ...
    # }

    # dimensions: ((tlx, tly), (brx, bry))
    # construct panel fragment
    panel = Image.new('RGBA',
                      (dimensions[1][0] - dimensions[0][0],
                       dimensions[1][1] - dimensions[0][1]),
                      color=(255, 255, 255))
    # draw figures on panel
    for fig in figures:
        drawFigure(figures[fig]['images'], panel, figures[fig])

    # draw dialogs (WIP)
    drawDialogs(panel, dialogs, figures, cast)

    # apply panel
    paste(panel, canvas, dimensions[0])

    # draw panel borderline
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(dimensions, outline='black', width=2)
