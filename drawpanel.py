from PIL import Image, ImageDraw
from drawfigure import drawFigure, paste


def drawPanel(canvas: Image, dimensions: tuple, figures: list):
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

    # TODO: draw dialogs
    # huge pain

    # apply panel
    paste(panel, canvas, dimensions[0])

    # draw panel borderline
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(dimensions, outline='black', width=2)


'''
cueball_ims = {
    'head': Image.open('./components/body/cueball.png'),
    'body': Image.open('./components/body/body.png'),
    'arm': Image.open('./components/body/arm.png'),
    'leg': Image.open('./components/body/leg.png')
}

cueball_params = {
    'meta': {'scale': 0.3},
    'neck': (100, 285),
    'head': {'theta': 0, 'direction': 'l', 'scale': 3.33},
    'body': {'theta': -5},
    'arms': {'thetas': [(30, 150), (-45, -135)], 'scale': 1},
    'legs': {'thetas': [(15, 10), (-15, -10)]}
}

figures = [{
    'ims': cueball_ims,
    'params': cueball_params
}]
'''



