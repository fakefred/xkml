from PIL import Image, ImageDraw
from drawtext import drawText
from utils import getValueOrFallback
from math import sin, cos


def connect(points: tuple):
    pass


def drawDialogs(canvas: Image, dialogs: dict, figures: dict, cast: dict):
    # create dialogs mask
    mask = Image.new('RGBA', canvas.size, color=(255, 255, 255, 0))
    # calculate dock point of figure
    # i.e. where to finally connect the text with the head
    for name in figures:
        fig = figures[name]
        figures[name]['dialogs'] = {}
        # extract position of top of head
        # which is where the bottom of the dialogs will be placed
        x, y = fig['neck']
        l = fig['images']['head'].size[0] * getValueOrFallback(
            cast[name], ['scaling', 'global'], 1
        ) * getValueOrFallback(
            cast[name], ['scaling', 'head'], 1
        )  # scaled head size
        theta = getValueOrFallback(fig['head'], 'theta', 0)
        # number of pixels to shift the dock point from the top of the head
        SHIFT = 10
        figures[name]['dialogs']['dock'] = (
            x-(l+SHIFT)*sin(theta), y-(l+SHIFT)*cos(theta))

        # fragment = canvas
        # draw = ImageDraw.Draw(fragment)
        # draw.point(figures[name]['dialogs']['dock'], fill='black')
        # fragment.show()

    # parse dialogs and count unique names
    figure_names = []
    parsed_dialogs = []
    for line_num in dialogs:
        line = dialogs[line_num]
        name = line.split(':')[0].strip()
        text = ''
        for substr in line.split(':')[1:]:
            text += substr + ':'
        text = text[:-1].strip()

        if name not in figure_names:
            figure_names.append(name)

        parsed_dialogs.append((name, text))

    dialogs = parsed_dialogs

    HORIZONTAL_MARGIN = 10
    TOP_MARGIN = 10
    COMPONENTS_PADDING = 20  # padding between texts and connectors
    w, h = canvas.size

    if len(figure_names) == 1:
        # single figure
        # speech takes up entire panel width
        figures[figure_names[0]]['dialogs']['l'] = HORIZONTAL_MARGIN
        figures[figure_names[0]]['dialogs']['w'] = w - 2 * HORIZONTAL_MARGIN
    elif len(figure_names) == 2:
        # two figures
        # speech takes up 2/3 of panel width above their respective heads
        leftmost = HORIZONTAL_MARGIN
        onethird = round(w / 3)
        twothirds = round(2 * w / 3)
        # figure out who's on the left and who's on the right
        fig0_x_axis = figures[figure_names[0]]['neck'][0]
        fig1_x_axis = figures[figure_names[1]]['neck'][0]

        figures[figure_names[0]]['dialogs']['w'] = twothirds
        figures[figure_names[1]]['dialogs']['w'] = twothirds

        if fig0_x_axis <= fig1_x_axis:
            # gotta put up with asymmetry to a certain degree
            # fig0 is on the left
            figures[figure_names[0]]['dialogs']['l'] = leftmost
            figures[figure_names[1]]['dialogs']['l'] = onethird
        else:
            # fig1 is on the left
            figures[figure_names[0]]['dialogs']['l'] = onethird
            figures[figure_names[1]]['dialogs']['l'] = leftmost
    # TODO: support more speakers

    # create a dict to hold figure data
    figs = {}
    for name in figure_names:
        figs[name] = {
            'initial_line': False,
            'initial_line_of_figure': True,
            'head_dock_point': figures[name]['dialogs']['dock'],
            # where the figure's next connector should be connected to
            'current_node_point': (0, 0),
            'l': figures[name]['dialogs']['l'],
            'w': figures[name]['dialogs']['w']
        }

    # `figure_names` is in the order of first speech
    figs[figure_names[0]]['initial_line'] = True

    # draw texts and connectors
    current_y = TOP_MARGIN
    # `dialogs` is now a list of (name, text) tuples
    for line in dialogs:
        name, text = line
        position = (figs[name]['l'], current_y)
        text_size = drawText(mask, text, position, maxwidth=figs[name]['w'])
        current_y += text_size[1] + COMPONENTS_PADDING

    # mask.show()
    canvas.paste(mask, (0, 0, w, h), mask=mask)
    # canvas.show()
