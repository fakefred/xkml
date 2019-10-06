from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math
import mathutils
from mathutils import abs_sin as sin, abs_cos as cos
from utils import getValueOrFallback


def paste(im: Image, canvas: Image, position: tuple):
    # places im on canvas(Image object) at position (x, y)
    canvas.paste(im, box=position, mask=im)


def drawHead(im: Image, canvas: Image, neck: tuple, theta: int, direction: str, scale=1.0):
    # neck: (x, y)
    # stationary point for the stick figure
    # theta: in integer degrees, within [-90, 90]
    # positive is counter-clockwise (to the left)
    im_scaled = im.resize((round(im.size[0] * scale),
                           round(im.size[1] * scale)))

    if direction in ['left', 'l']:
        im_flipped = im_scaled.transpose(method=Image.FLIP_LEFT_RIGHT)
    else:
        im_flipped = im_scaled

    im_rotated = im_flipped.rotate(theta, expand=True, resample=Image.BICUBIC)

    w, h = im_scaled.size
    x, y = neck
    theta = mathutils.normalize_into_interval(theta, (-90, 90))
    # determine where to *actually* paste the head on the cartesian plane
    # sin and cos are abs'd because negative numbers are complicated
    if 0 <= theta <= 90:
        top_left = (round(x-1/2*w*cos(theta)-h*sin(theta)),
                    round(y-1/2*w*sin(theta)-h*cos(theta)))
    elif -90 <= theta < 0:
        top_left = (round(x-1/2*w*cos(theta)),
                    round(y-1/2*w*sin(theta)-h*cos(theta)))

    paste(im_rotated, canvas, top_left)


def drawLine(im: Image, canvas: Image, point: tuple, theta: int, scale=1.0):
    # im: assumed to be a line; width ignored
    # theta: int deg, within [-90, 90]
    # positive is counter-clockwise (to the right)
    im_rotated = im.rotate(theta, expand=True, resample=Image.BICUBIC)
    # im_enhanced = im_rotated.filter(ImageFilter.SMOOTH)
    im_scaled = im_rotated.resize((round(im_rotated.size[0] * scale),
                                   round(im_rotated.size[1] * scale)))
    h = im.size[1] * scale
    x, y = point
    theta = mathutils.normalize_into_interval(theta, (-180, 180))
    if 0 <= theta <= 90:
        top_left = point
    elif 90 < theta <= 180:
        top_left = (x, round(y-h*cos(theta)))
    elif -90 <= theta < 0:
        top_left = (round(x-h*sin(theta)), y)
    elif -180 <= theta < -90:
        top_left = (round(x-h*sin(theta)), round(y-h*cos(theta)))

    paste(im_scaled, canvas, top_left)

    # returns the endpoint of the line
    return (round(x+h*math.sin(math.radians(theta))),
            round(y+h*math.cos(math.radians(theta))))


def drawBody(im: Image, canvas: Image, neck: tuple, theta: int, scale=1.0):
    # returns (x, y) of waist
    return drawLine(im, canvas, neck, theta, scale)


def drawLimbs(im: Image, canvas: Image, neck_or_waist: tuple, theta_pairs: list, scale=1.0):
    # theta_pairs: list containing theta's of all of your arms/legs
    # yes, *all* of them, the list can be of arbitrary length, including zero
    # example
    # [(arm0_upper_theta, arm0_fore_theta), (arm1_upper_theta, arm1_fore_theta), ...]
    x, y = neck_or_waist
    h = im.size[1] * scale
    for thetas in theta_pairs.values():
        # draw upper arm / upper leg (thigh) first
        drawLine(im, canvas, neck_or_waist, thetas[0], scale)

        # determine location of the elbow/knee
        elbow_or_knee = (round(x+h*math.sin(math.radians(thetas[0]))),
                         round(y+h*math.cos(math.radians(thetas[0]))))

        # draw forearm / lower leg
        drawLine(im, canvas, elbow_or_knee, thetas[1], scale)


def drawFigure(ims: dict, canvas: Image, params: dict):
    # ims: image objects for different body parts
    scaling = {
        'global': getValueOrFallback(params, ['scaling', 'global'], 1),
        'head': getValueOrFallback(params, ['scaling', 'head'], 1),
        'body': getValueOrFallback(params, ['scaling', 'body'], 1),
        'arms': getValueOrFallback(params, ['scaling', 'arms'], 1),
        'legs': getValueOrFallback(params, ['scaling', 'legs'], 1)
    }

    # head
    drawHead(ims['head'], canvas, params['neck'],
             getValueOrFallback(params, ['head', 'theta'], 0),
             getValueOrFallback(params, ['head', 'direction'], 'right'),
             scaling['global'] * scaling['head'])

    # body
    waist = drawBody(ims['body'], canvas, params['neck'],
                     getValueOrFallback(params, ['body', 'theta'], 0),
                     scaling['global'])

    # arms
    drawLimbs(ims['arm'], canvas, params['neck'],
              getValueOrFallback(params, ['arms', 'thetas'], 0),
              scaling['global'])

    # legs
    drawLimbs(ims['leg'], canvas, waist,
              getValueOrFallback(params, ['legs', 'thetas'], 0),
              scaling['global'])


'''
xkcd_font = ImageFont.truetype('./xkcd_script.ttf', 25)
draw_on_canvas = ImageDraw.Draw(canvas)
draw_on_canvas.text((15, 15), 'XKML: \nWHAT COULD GO WRONG?',
                    fill=(0, 0, 0, 255), font=xkcd_font)


# canvas.save('out.png')
canvas.show()
'''
