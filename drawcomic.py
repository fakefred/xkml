from PIL import Image, ImageDraw
from drawpanel import drawPanel
from drawtext import drawText
from utils import getValueOrFallback
from parser import parse as parseXKML

'''
comic dict for test use.
------
comic = {
    'meta': {
        'title': 'Some Title, I Guess?',
        'author': 'fkfd'
    },
    'comic': {
        'cast': {
            'cueball': {
                'images': {
                    'head': './components/body/cueball.png',
                    'body': './components/body/body.png',
                    'arm': './components/body/arm.png',
                    'leg': './components/body/leg.png'},
                'scaling': {'global': 0.3, 'head': 3.33}
            },
            'megan': {
                'images': {
                    'head': './components/body/cueball.png',
                    'body': './components/body/body.png',
                    'arm': './components/body/arm.png',
                    'leg': './components/body/leg.png'
                },
                'scaling': {'global': 0.3, 'head': 3.33}
            }
        },
        'panels': {
            0: {
                'position': (10, 10),
                'size': (310, 380),
                'figures': {
                    'cueball': {
                        'neck': (100, 285),
                        'head': {
                            'theta': 0,
                            'direction': 'r'
                        },
                        'body': {'theta': -5},
                        'arms': {
                            'thetas': {
                                0: (-45, -135),
                                1: (30, 150)
                            }
                        },
                        'legs': {
                            'thetas': {
                                0: (-15, -10),
                                1: (15, 10)
                            }
                        }
                    }
                }
            }, 1: {
                'position': (330, 10),
                'size': (310, 380),
                'figures': {
                    'cueball': {
                        'neck': (100, 285),
                        'head': {
                            'theta': 0,
                            'direction': 'l'
                        },
                        'body': {
                            'theta': 0
                        },
                        'arms': {
                            'thetas': {
                                0: (-15, -15),
                                1: (15, 15)
                            }
                        },
                        'legs': {
                            'thetas': {
                                0: (-15, -10),
                                1: (15, 10)
                            }
                        }
                    }
                }
            }
        }
    }
}
'''


def drawComic(xkml):
    comic = parseXKML(xkml)
    canvas = Image.new('RGB', comic['meta']['size'], color=(255, 255, 255))

    panels = comic['comic']['panels']
    for panel in panels.values():
        for fig in panel['figures']:
            # assign images defined in cast to each figure
            fig_img_strs = comic['comic']['cast'][fig]['images']
            panel['figures'][fig]['images'] = {}
            for body_part in fig_img_strs:
                panel['figures'][fig]['images'][body_part] = Image.open(
                    fig_img_strs[body_part])
            # assign scale to each body part
            panel['figures'][fig]['scaling'] = comic['comic']['cast'][fig]['scaling']
        drawPanel(canvas,
                  (panel['position'],
                   (panel['position'][0] + panel['size'][0],
                    panel['position'][1] + panel['size'][1])
                   ),
                  panel['figures'], panel['dialogs'], comic['comic']['cast'])
    canvas.show()
