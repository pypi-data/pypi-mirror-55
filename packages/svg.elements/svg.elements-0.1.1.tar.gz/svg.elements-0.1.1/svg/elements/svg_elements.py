from __future__ import division

import re
from collections import MutableSequence
from copy import copy
from math import *
from xml.etree.ElementTree import iterparse

try:
    from math import tau
except ImportError:
    tau = pi * 2

"""
The path elements are derived from regebro's svg.path project ( https://github.com/regebro/svg.path ) with
some of the math from mathandy's svgpathtools project ( https://github.com/mathandy/svgpathtools ).

The Zingl-Bresenham plotting algorithms are from Alois Zingl's "The Beauty of Bresenham's Algorithm"
( http://members.chello.at/easyfilter/bresenham.html ). They are all MIT Licensed and this library is
also MIT licensed. In the case of Zingl's work this isn't explicit from his website, however from personal
correspondence "'Free and open source' means you can do anything with it like the MIT licence."

The goal is to provide svg like path objects and structures. The svg standard 1.1 and elements of 2.0 will
be used to provide much of the decisions within path objects. Such that if there is a question on
implementation if the SVG documentation has a methodology it should be used.
"""

MIN_DEPTH = 5
ERROR = 1e-12

max_depth = 0

# SVG STATIC VALUES
SVG_NAME_TAG = 'svg'
SVG_ATTR_VERSION = 'version'
SVG_VALUE_VERSION = '1.1'
SVG_ATTR_XMLNS = 'xmlns'
SVG_VALUE_XMLNS = 'http://www.w3.org/2000/svg'
SVG_ATTR_XMLNS_LINK = 'xmlns:xlink'
SVG_VALUE_XLINK = 'http://www.w3.org/1999/xlink'
SVG_ATTR_XMLNS_EV = 'xmlns:ev'
SVG_VALUE_XMLNS_EV = 'http://www.w3.org/2001/xml-events'

XLINK_HREF = '{http://www.w3.org/1999/xlink}href'
SVG_HREF = "href"
SVG_ATTR_WIDTH = 'width'
SVG_ATTR_HEIGHT = 'height'
SVG_ATTR_VIEWBOX = 'viewBox'
SVG_VIEWBOX_TRANSFORM = 'viewbox_transform'
SVG_TAG_PATH = 'path'
SVG_TAG_GROUP = 'g'
SVG_TAG_RECT = 'rect'
SVG_TAG_CIRCLE = 'circle'
SVG_TAG_ELLIPSE = 'ellipse'
SVG_TAG_LINE = 'line'
SVG_TAG_POLYLINE = 'polyline'
SVG_TAG_POLYGON = 'polygon'
SVG_TAG_TEXT = 'text'
SVG_TAG_IMAGE = 'image'
SVG_TAG_DESC = 'desc'
SVG_ATTR_DATA = 'd'
SVG_ATTR_FILL = 'fill'
SVG_ATTR_STROKE = 'stroke'
SVG_ATTR_STROKE_WIDTH = 'stroke-width'
SVG_ATTR_TRANSFORM = 'transform'
SVG_ATTR_STYLE = 'style'
SVG_ATTR_CENTER_X = 'cx'
SVG_ATTR_CENTER_Y = 'cy'
SVG_ATTR_RADIUS_X = 'rx'
SVG_ATTR_RADIUS_Y = 'ry'
SVG_ATTR_RADIUS = 'r'
SVG_ATTR_POINTS = 'points'
SVG_ATTR_PRESERVEASPECTRATIO = 'preserveAspectRatio'
SVG_ATTR_X = 'x'
SVG_ATTR_Y = 'y'
SVG_ATTR_TAG = 'tag'
SVG_TRANSFORM_MATRIX = 'matrix'
SVG_TRANSFORM_TRANSLATE = 'translate'
SVG_TRANSFORM_SCALE = 'scale'
SVG_TRANSFORM_ROTATE = 'rotate'
SVG_TRANSFORM_SKEW_X = 'skewx'
SVG_TRANSFORM_SKEW_Y = 'skewy'
SVG_TRANSFORM_SKEW = 'skew'
SVG_TRANSFORM_TRANSLATE_X = 'translatex'
SVG_TRANSFORM_TRANSLATE_Y = 'translatey'
SVG_TRANSFORM_SCALE_X = 'scalex'
SVG_TRANSFORM_SCALE_Y = 'scaley'
SVG_VALUE_NONE = 'none'

PATTERN_WS = r'[\s\t\n]*'
PATTERN_COMMA = r'(?:\s*,\s*|\s+|(?=-))'
PATTERN_FLOAT = '[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
PATTERN_LENGTH_UNITS = 'cm|mm|Q|in|pt|pc|px|em|cx|ch|rem|vw|vh|vmin|vmax'
PATTERN_ANGLE_UNITS = 'deg|grad|rad|turn'
PATTERN_TIME_UNITS = 's|ms'
PATTERN_FREQUENCY_UNITS = 'Hz|kHz'
PATTERN_RESOLUTION_UNITS = 'dpi|dpcm|dppx'
PATTERN_PERCENT = '%'
PATTERN_TRANSFORM = SVG_TRANSFORM_MATRIX + '|' \
                    + SVG_TRANSFORM_TRANSLATE + '|' \
                    + SVG_TRANSFORM_TRANSLATE_X + '|' \
                    + SVG_TRANSFORM_TRANSLATE_Y + '|' \
                    + SVG_TRANSFORM_SCALE + '|' \
                    + SVG_TRANSFORM_SCALE_X + '|' \
                    + SVG_TRANSFORM_SCALE_Y + '|' \
                    + SVG_TRANSFORM_ROTATE + '|' \
                    + SVG_TRANSFORM_SKEW + '|' \
                    + SVG_TRANSFORM_SKEW_X + '|' \
                    + SVG_TRANSFORM_SKEW_Y
PATTERN_TRANSFORM_UNITS = PATTERN_LENGTH_UNITS + '|' \
                          + PATTERN_ANGLE_UNITS + '|' \
                          + PATTERN_PERCENT

REGEX_FLOAT = re.compile(PATTERN_FLOAT)
REGEX_COORD_PAIR = re.compile('(%s)%s(%s)' % (PATTERN_FLOAT, PATTERN_COMMA, PATTERN_FLOAT))
REGEX_TRANSFORM_TEMPLATE = re.compile('(?u)(%s)%s\(([^)]+)\)' % (PATTERN_TRANSFORM, PATTERN_WS))
REGEX_TRANSFORM_PARAMETER = re.compile('(%s)%s(%s)?' % (PATTERN_FLOAT, PATTERN_WS, PATTERN_TRANSFORM_UNITS))


# Leaf node to pathd values.

def path2pathd(path):
    return path.get(SVG_ATTR_DATA, '')


def ellipse2pathd(ellipse):
    """converts the parameters from an ellipse or a circle to a string for a
    Path object d-attribute"""

    cx = ellipse.get(SVG_ATTR_CENTER_X, None)
    cy = ellipse.get(SVG_ATTR_CENTER_Y, None)
    rx = ellipse.get(SVG_ATTR_RADIUS_X, None)
    ry = ellipse.get(SVG_ATTR_RADIUS_X, None)
    r = ellipse.get(SVG_ATTR_RADIUS, None)

    if r is not None:
        rx = ry = float(r)
    else:
        rx = float(rx)
        ry = float(ry)

    cx = float(cx)
    cy = float(cy)

    d = ''
    d += 'M' + str(cx - rx) + ',' + str(cy)
    d += 'a' + str(rx) + ',' + str(ry) + ' 0 1,0 ' + str(2 * rx) + ',0'
    d += 'a' + str(rx) + ',' + str(ry) + ' 0 1,0 ' + str(-2 * rx) + ',0'

    return d


def polyline2pathd(polyline, is_polygon=False):
    """converts the string from a polyline parameters to a string for a
    Path object d-attribute"""
    polyline_d = polyline.get(SVG_ATTR_POINTS, None)
    if polyline_d is None:
        return ''
    points = REGEX_COORD_PAIR.findall(polyline_d)
    closed = (float(points[0][0]) == float(points[-1][0]) and
              float(points[0][1]) == float(points[-1][1]))

    # The `parse_path` call ignores redundant 'z' (closure) commands
    # e.g. `parse_path('M0 0L100 100Z') == parse_path('M0 0L100 100L0 0Z')`
    # This check ensures that an n-point polygon is converted to an n-Line path.
    if is_polygon and closed:
        points.append(points[0])

    d = 'M' + 'L'.join('{0} {1}'.format(x, y) for x, y in points)
    if is_polygon or closed:
        d += 'z'
    return d


def polygon2pathd(polyline):
    """converts the string from a polygon parameters to a string
    for a Path object d-attribute.
    Note:  For a polygon made from n points, the resulting path will be
    composed of n lines (even if some of these lines have length zero).
    """
    return polyline2pathd(polyline, True)


def rect2pathd(rect):
    """Converts an SVG-rect element to a Path d-string.

    The rectangle will start at the (x,y) coordinate specified by the
    rectangle object and proceed counter-clockwise."""
    x0, y0 = float(rect.get(SVG_ATTR_X, 0)), float(rect.get(SVG_ATTR_Y, 0))
    w, h = float(rect.get(SVG_ATTR_WIDTH, 0)), float(rect.get(SVG_ATTR_HEIGHT, 0))
    x1, y1 = x0 + w, y0
    x2, y2 = x0 + w, y0 + h
    x3, y3 = x0, y0 + h

    d = ("M{} {} L {} {} L {} {} L {} {} z"
         "".format(x0, y0, x1, y1, x2, y2, x3, y3))
    return d


def line2pathd(l):
    return 'M' + l['x1'] + ' ' + l['y1'] + 'L' + l['x2'] + ' ' + l['y2']


# PathTokens class.
class PathTokens:
    """Path Tokens is the class for the general outline of how SVG Pathd objects
    are stored. Namely, a single non-'e' character and a collection of floating
    point numbers. While this is explicitly used for SVG pathd objects the method
    for serializing command data in this fashion is also useful as a standalone
    class."""

    def __init__(self, command_elements):
        self.command_elements = command_elements
        commands = ''
        for k in command_elements:
            commands += k
        self.COMMAND_RE = re.compile("([%s])" % (commands))
        self.elements = None
        self.command = None
        self.last_command = None
        self.parser = None

    def _tokenize_path(self, pathdef):
        for x in self.COMMAND_RE.split(pathdef):
            if x in self.command_elements:
                yield x
            for token in REGEX_FLOAT.findall(x):
                yield token

    def get(self):
        """Gets the element from the stack."""
        return self.elements.pop()

    def pre_execute(self):
        """Called before any command element is executed."""
        pass

    def post_execute(self):
        """Called after any command element is executed."""
        pass

    def new_command(self):
        """Called when command element is switched."""
        pass

    def parse(self, pathdef):
        self.elements = list(self._tokenize_path(pathdef))
        # Reverse for easy use of .pop()
        self.elements.reverse()

        while self.elements:
            if self.elements[-1] in self.command_elements:
                self.last_command = self.command
                self.command = self.get()
                self.new_command()
            else:
                if self.command is None:
                    raise ValueError("Invalid command.")  # could be faulty implicit or unaccepted element.
            self.pre_execute()
            self.command_elements[self.command]()
            self.post_execute()


# SVG Path Tokens.
class SVGPathTokens(PathTokens):
    """Utilizes the general PathTokens class to parse SVG pathd strings.
    This class has been updated to account for SVG 2.0 version of the zZ command."""

    def __init__(self):
        PathTokens.__init__(self, {
            'M': self.move_to,
            'm': self.move_to,
            'L': self.line_to,
            'l': self.line_to,
            "H": self.h_to,
            "h": self.h_to,
            "V": self.v_to,
            "v": self.v_to,
            "C": self.cubic_to,
            "c": self.cubic_to,
            "S": self.smooth_cubic_to,
            "s": self.smooth_cubic_to,
            "Q": self.quad_to,
            "q": self.quad_to,
            "T": self.smooth_quad_to,
            "t": self.smooth_quad_to,
            "A": self.arc_to,
            "a": self.arc_to,
            "Z": self.close,
            "z": self.close
        })
        self.parser = None
        self.absolute = False

    def svg_parse(self, parser, pathdef):
        self.parser = parser
        self.absolute = False
        self.parser.start()
        self.parse(pathdef)
        self.parser.end()

    def get_pos(self):
        if self.command == 'Z':
            return "z"  # After Z, all further expected values are also Z.
        coord0 = self.get()
        if coord0 == 'z' or coord0 == 'Z':
            self.command = 'Z'
            return "z"
        coord1 = self.get()
        position = (float(coord0), float(coord1))
        if not self.absolute:
            current_pos = self.parser.current_point
            if current_pos is None:
                return position
            return [position[0] + current_pos[0], position[1] + current_pos[1]]
        return position

    def move_to(self):
        # Moveto command.
        pos = self.get_pos()
        self.parser.move(pos)

        # Implicit moveto commands are treated as lineto commands.
        # So we set command to lineto here, in case there are
        # further implicit commands after this moveto.
        self.command = 'L'

    def line_to(self):
        pos = self.get_pos()
        self.parser.line(pos)

    def h_to(self):
        x = float(self.get())
        if self.absolute:
            self.parser.absolute_h(x)
        else:
            self.parser.relative_h(x)

    def v_to(self):
        y = float(self.get())
        if self.absolute:
            self.parser.absolute_v(y)
        else:
            self.parser.relative_v(y)

    def cubic_to(self):
        control1 = self.get_pos()
        control2 = self.get_pos()
        end = self.get_pos()
        self.parser.cubic(control1, control2, end)

    def smooth_cubic_to(self):
        control2 = self.get_pos()
        end = self.get_pos()
        self.parser.smooth_cubic(control2, end)

    def quad_to(self):
        control = self.get_pos()
        end = self.get_pos()
        self.parser.quad(control, end)

    def smooth_quad_to(self):
        end = self.get_pos()
        self.parser.smooth_quad(end)

    def arc_to(self):
        rx = float(self.get())
        ry = float(self.get())
        rotation = float(self.get())
        arc = float(self.get())
        sweep = float(self.get())
        end = self.get_pos()

        self.parser.arc(rx, ry, rotation, arc, sweep, end)

    def close(self):
        # Close path
        self.parser.closed()
        self.command = None

    def new_command(self):
        self.absolute = self.command.isupper()

    def post_execute(self):
        pass


def parse_viewbox_transform(svg_node, ppi=96.0, viewbox=None):
    """
    SVG 1.1 7.2, SVG 2.0 8.2 equivalent transform of an SVG viewport.
    With regards to https://github.com/w3c/svgwg/issues/215 use 8.2 version.

    It creates a matrix equal to that viewport expected.

    :param svg_node: dict containing the relevant svg entries.
    :return: string of the SVG transform commands to account for the viewbox.
    """
    if viewbox is None:
        if SVG_ATTR_VIEWBOX in svg_node:
            # Let vb-x, vb-y, vb-width, vb-height be the min-x, min-y,
            # width and height values of the viewBox attribute respectively.
            viewbox = svg_node[SVG_ATTR_VIEWBOX]
        else:
            viewbox = "0 0 100 100"
    # Let e-x, e-y, e-width, e-height be the position and size of the element respectively.
    vb = viewbox.split(" ")
    vb_x = float(vb[0])
    vb_y = float(vb[1])
    vb_width = float(vb[2])
    vb_height = float(vb[3])
    if SVG_ATTR_X in svg_node:
        e_x = Distance.parse(svg_node[SVG_ATTR_X], ppi)
    else:
        e_x = 0
    if SVG_ATTR_Y in svg_node:
        e_y = Distance.parse(svg_node[SVG_ATTR_Y], ppi)
    else:
        e_y = 0
    if SVG_ATTR_WIDTH in svg_node:
        e_width = Distance.parse(svg_node[SVG_ATTR_WIDTH], ppi)
    else:
        e_width = 100.0
    if SVG_ATTR_HEIGHT in svg_node:
        e_height = Distance.parse(svg_node[SVG_ATTR_HEIGHT], ppi)
    else:
        e_height = e_width

    # Let align be the align value of preserveAspectRatio, or 'xMidYMid' if preserveAspectRatio is not defined.
    # Let meetOrSlice be the meetOrSlice value of preserveAspectRatio, or 'meet' if preserveAspectRatio is not defined
    # or if meetOrSlice is missing from this value.
    if SVG_ATTR_PRESERVEASPECTRATIO in svg_node:
        aspect = svg_node[SVG_ATTR_PRESERVEASPECTRATIO]
        aspect_slice = aspect.split(' ')
        try:
            align = aspect_slice[0]
        except IndexError:
            align = 'xMidYMid'
        try:
            meet_or_slice = aspect_slice[1]
        except IndexError:
            meet_or_slice = 'meet'
    else:
        align = 'xMidYMid'
        meet_or_slice = 'meet'

    # Initialize scale-x to e-width/vb-width.
    scale_x = e_width / vb_width
    # Initialize scale-y to e-height/vb-height.
    scale_y = e_height / vb_height

    # If align is not 'none' and meetOrSlice is 'meet', set the larger of scale-x and scale-y to the smaller.
    if align != SVG_VALUE_NONE and meet_or_slice == 'meet':
        scale_x = max(scale_x, scale_y)
        scale_y = scale_x
    # Otherwise, if align is not 'none' and meetOrSlice is 'slice', set the smaller of scale-x and scale-y to the larger
    elif align != SVG_VALUE_NONE and meet_or_slice == 'slice':
        scale_x = min(scale_x, scale_y)
        scale_y = scale_x
    # Initialize translate-x to e-x - (vb-x * scale-x).
    translate_x = e_x - (vb_x * scale_x)
    # Initialize translate-y to e-y - (vb-y * scale-y)
    translate_y = e_y - (vb_y * scale_y)
    # If align contains 'xMid', add (e-width - vb-width * scale-x) / 2 to translate-x.
    align = align.lower()
    if 'xmid' in align:
        translate_x += (e_width - vb_width * scale_x) / 2.0
    # If align contains 'xMax', add (e-width - vb-width * scale-x) to translate-x.
    if 'xmax' in align:
        translate_x += e_width - vb_width * scale_x
    # If align contains 'yMid', add (e-height - vb-height * scale-y) / 2 to translate-y.
    if 'ymid' in align:
        translate_y += (e_height - vb_height * scale_y) / 2.0
    # If align contains 'yMax', add (e-height - vb-height * scale-y) to translate-y.
    if 'ymax' in align:
        translate_y += (e_height - vb_height * scale_y)

    if translate_x == 0 and translate_y == 0:
        if scale_x == 1 and scale_y == 1:
            return ""  # Nothing happens.
        else:
            return "scale(%f, %f)" % (scale_x, scale_y)
    else:
        if scale_x == 1 and scale_y == 1:
            return "translate(%f, %f)" % (translate_x, translate_y)
        else:
            return "translate(%f, %f) scale(%f, %f)" % (translate_x, translate_y, scale_x, scale_y)
            # return "scale(%f, %f) translate(%f, %f)" % (scale_x, scale_y, translate_x, translate_y)


class Distance(float):
    """CSS Distance defines as used in SVG"""

    def __repr__(self):
        return "Distance(%.12f)" % self

    @classmethod
    def parse(cls, distance_str, ppi=96.0):
        """Convert svg length to set distances.
        96 is the typical pixels per inch.
        Other values have been used."""

        if not isinstance(distance_str, str):
            return float(distance_str)
        if distance_str.endswith('mm'):
            return Distance.mm(float(distance_str[:-2]))
        if distance_str.endswith('cm'):
            return Distance.cm(float(distance_str[:-2]))
        if distance_str.endswith('in'):
            return Distance.inch(float(distance_str[:-2]))
        if distance_str.endswith('px'):
            return Distance.px(float(distance_str[:-2]))
        if distance_str.endswith('pt'):
            return Distance.pt(float(distance_str[:-2]))
        if distance_str.endswith('pc'):
            return Distance.pc(float(distance_str[:-2]))
        return float(distance_str)

    @classmethod
    def mm(cls, value, ppi=96.0):
        return cls(value * ppi * 0.0393701)

    @classmethod
    def cm(cls, value, ppi=96.0):
        return cls(value * ppi * 0.393701)

    @classmethod
    def inch(cls, value, ppi=96.0):
        return cls(value * ppi)

    @classmethod
    def px(cls, value, ppi=96.0):
        return cls(value)

    @classmethod
    def pt(cls, value, ppi=96.0):
        return cls(value * 1.3333)

    @classmethod
    def pc(cls, value, ppi=96.0):
        return cls(value * 16)

    @property
    def as_mm(self, ppi=96.0):
        return float(self) / (ppi * 0.0393701)

    @property
    def as_cm(self, ppi=96.0):
        return float(self) / (ppi * 0.393701)

    @property
    def as_inch(self, ppi=96.0):
        return float(self) / ppi


# SVG Color Parsing

# defining predefined colors permitted by svg: https://www.w3.org/TR/SVG11/types.html#ColorKeywords

class Color(int):

    def __repr__(self):
        return "Color(%d)" % self

    @classmethod
    def parse(cls, color_string):
        """Parse SVG color, will return a set value."""
        hex_re = re.compile(r'^#?([0-9A-Fa-f]{3,8})$')
        match = hex_re.match(color_string)
        if match:
            return Color.parse_color_hex(color_string)
        rgb_re = re.compile(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)')
        match = rgb_re.match(color_string)
        if match:
            return Color.parse_color_rgb(match.groups())

        rgbp_re = re.compile(r'rgb\(\s*(\d+)%\s*,\s*(\d+)%\s*,\s*(\d+)%\s*\)')
        match = rgbp_re.match(color_string)
        if match:
            return Color.parse_color_rgbp(match.groups())
        return Color.parse_color_lookup(color_string)

    @classmethod
    def rgb(cls, r, g, b):
        return cls(int(0xFF000000 |
                       ((r & 255) << 16) |
                       ((g & 255) << 8) |
                       (b & 255)))

    @classmethod
    def parse_color_lookup(cls, v):
        """Parse SVG Color by Keyword on dictionary lookup"""
        if v == "aliceblue":
            return Color.rgb(250, 248, 255)
        if v == "aliceblue":
            return Color.rgb(240, 248, 255)
        if v == "antiquewhite":
            return Color.rgb(250, 235, 215)
        if v == "aqua":
            return Color.rgb(0, 255, 255)
        if v == "aquamarine":
            return Color.rgb(127, 255, 212)
        if v == "azure":
            return Color.rgb(240, 255, 255)
        if v == "beige":
            return Color.rgb(245, 245, 220)
        if v == "bisque":
            return Color.rgb(255, 228, 196)
        if v == "black":
            return Color.rgb(0, 0, 0)
        if v == "blanchedalmond":
            return Color.rgb(255, 235, 205)
        if v == "blue":
            return Color.rgb(0, 0, 255)
        if v == "blueviolet":
            return Color.rgb(138, 43, 226)
        if v == "brown":
            return Color.rgb(165, 42, 42)
        if v == "burlywood":
            return Color.rgb(222, 184, 135)
        if v == "cadetblue":
            return Color.rgb(95, 158, 160)
        if v == "chartreuse":
            return Color.rgb(127, 255, 0)
        if v == "chocolate":
            return Color.rgb(210, 105, 30)
        if v == "coral":
            return Color.rgb(255, 127, 80)
        if v == "cornflowerblue":
            return Color.rgb(100, 149, 237)
        if v == "cornsilk":
            return Color.rgb(255, 248, 220)
        if v == "crimson":
            return Color.rgb(220, 20, 60)
        if v == "cyan":
            return Color.rgb(0, 255, 255)
        if v == "darkblue":
            return Color.rgb(0, 0, 139)
        if v == "darkcyan":
            return Color.rgb(0, 139, 139)
        if v == "darkgoldenrod":
            return Color.rgb(184, 134, 11)
        if v == "darkgray":
            return Color.rgb(169, 169, 169)
        if v == "darkgreen":
            return Color.rgb(0, 100, 0)
        if v == "darkgrey":
            return Color.rgb(169, 169, 169)
        if v == "darkkhaki":
            return Color.rgb(189, 183, 107)
        if v == "darkmagenta":
            return Color.rgb(139, 0, 139)
        if v == "darkolivegreen":
            return Color.rgb(85, 107, 47)
        if v == "darkorange":
            return Color.rgb(255, 140, 0)
        if v == "darkorchid":
            return Color.rgb(153, 50, 204)
        if v == "darkred":
            return Color.rgb(139, 0, 0)
        if v == "darksalmon":
            return Color.rgb(233, 150, 122)
        if v == "darkseagreen":
            return Color.rgb(143, 188, 143)
        if v == "darkslateblue":
            return Color.rgb(72, 61, 139)
        if v == "darkslategray":
            return Color.rgb(47, 79, 79)
        if v == "darkslategrey":
            return Color.rgb(47, 79, 79)
        if v == "darkturquoise":
            return Color.rgb(0, 206, 209)
        if v == "darkviolet":
            return Color.rgb(148, 0, 211)
        if v == "deeppink":
            return Color.rgb(255, 20, 147)
        if v == "deepskyblue":
            return Color.rgb(0, 191, 255)
        if v == "dimgray":
            return Color.rgb(105, 105, 105)
        if v == "dimgrey":
            return Color.rgb(105, 105, 105)
        if v == "dodgerblue":
            return Color.rgb(30, 144, 255)
        if v == "firebrick":
            return Color.rgb(178, 34, 34)
        if v == "floralwhite":
            return Color.rgb(255, 250, 240)
        if v == "forestgreen":
            return Color.rgb(34, 139, 34)
        if v == "fuchsia":
            return Color.rgb(255, 0, 255)
        if v == "gainsboro":
            return Color.rgb(220, 220, 220)
        if v == "ghostwhite":
            return Color.rgb(248, 248, 255)
        if v == "gold":
            return Color.rgb(255, 215, 0)
        if v == "goldenrod":
            return Color.rgb(218, 165, 32)
        if v == "gray":
            return Color.rgb(128, 128, 128)
        if v == "grey":
            return Color.rgb(128, 128, 128)
        if v == "green":
            return Color.rgb(0, 128, 0)
        if v == "greenyellow":
            return Color.rgb(173, 255, 47)
        if v == "honeydew":
            return Color.rgb(240, 255, 240)
        if v == "hotpink":
            return Color.rgb(255, 105, 180)
        if v == "indianred":
            return Color.rgb(205, 92, 92)
        if v == "indigo":
            return Color.rgb(75, 0, 130)
        if v == "ivory":
            return Color.rgb(255, 255, 240)
        if v == "khaki":
            return Color.rgb(240, 230, 140)
        if v == "lavender":
            return Color.rgb(230, 230, 250)
        if v == "lavenderblush":
            return Color.rgb(255, 240, 245)
        if v == "lawngreen":
            return Color.rgb(124, 252, 0)
        if v == "lemonchiffon":
            return Color.rgb(255, 250, 205)
        if v == "lightblue":
            return Color.rgb(173, 216, 230)
        if v == "lightcoral":
            return Color.rgb(240, 128, 128)
        if v == "lightcyan":
            return Color.rgb(224, 255, 255)
        if v == "lightgoldenrodyellow":
            return Color.rgb(250, 250, 210)
        if v == "lightgray":
            return Color.rgb(211, 211, 211)
        if v == "lightgreen":
            return Color.rgb(144, 238, 144)
        if v == "lightgrey":
            return Color.rgb(211, 211, 211)
        if v == "lightpink":
            return Color.rgb(255, 182, 193)
        if v == "lightsalmon":
            return Color.rgb(255, 160, 122)
        if v == "lightseagreen":
            return Color.rgb(32, 178, 170)
        if v == "lightskyblue":
            return Color.rgb(135, 206, 250)
        if v == "lightslategray":
            return Color.rgb(119, 136, 153)
        if v == "lightslategrey":
            return Color.rgb(119, 136, 153)
        if v == "lightsteelblue":
            return Color.rgb(176, 196, 222)
        if v == "lightyellow":
            return Color.rgb(255, 255, 224)
        if v == "lime":
            return Color.rgb(0, 255, 0)
        if v == "limegreen":
            return Color.rgb(50, 205, 50)
        if v == "linen":
            return Color.rgb(250, 240, 230)
        if v == "magenta":
            return Color.rgb(255, 0, 255)
        if v == "maroon":
            return Color.rgb(128, 0, 0)
        if v == "mediumaquamarine":
            return Color.rgb(102, 205, 170)
        if v == "mediumblue":
            return Color.rgb(0, 0, 205)
        if v == "mediumorchid":
            return Color.rgb(186, 85, 211)
        if v == "mediumpurple":
            return Color.rgb(147, 112, 219)
        if v == "mediumseagreen":
            return Color.rgb(60, 179, 113)
        if v == "mediumslateblue":
            return Color.rgb(123, 104, 238)
        if v == "mediumspringgreen":
            return Color.rgb(0, 250, 154)
        if v == "mediumturquoise":
            return Color.rgb(72, 209, 204)
        if v == "mediumvioletred":
            return Color.rgb(199, 21, 133)
        if v == "midnightblue":
            return Color.rgb(25, 25, 112)
        if v == "mintcream":
            return Color.rgb(245, 255, 250)
        if v == "mistyrose":
            return Color.rgb(255, 228, 225)
        if v == "moccasin":
            return Color.rgb(255, 228, 181)
        if v == "navajowhite":
            return Color.rgb(255, 222, 173)
        if v == "navy":
            return Color.rgb(0, 0, 128)
        if v == "oldlace":
            return Color.rgb(253, 245, 230)
        if v == "olive":
            return Color.rgb(128, 128, 0)
        if v == "olivedrab":
            return Color.rgb(107, 142, 35)
        if v == "orange":
            return Color.rgb(255, 165, 0)
        if v == "orangered":
            return Color.rgb(255, 69, 0)
        if v == "orchid":
            return Color.rgb(218, 112, 214)
        if v == "palegoldenrod":
            return Color.rgb(238, 232, 170)
        if v == "palegreen":
            return Color.rgb(152, 251, 152)
        if v == "paleturquoise":
            return Color.rgb(175, 238, 238)
        if v == "palevioletred":
            return Color.rgb(219, 112, 147)
        if v == "papayawhip":
            return Color.rgb(255, 239, 213)
        if v == "peachpuff":
            return Color.rgb(255, 218, 185)
        if v == "peru":
            return Color.rgb(205, 133, 63)
        if v == "pink":
            return Color.rgb(255, 192, 203)
        if v == "plum":
            return Color.rgb(221, 160, 221)
        if v == "powderblue":
            return Color.rgb(176, 224, 230)
        if v == "purple":
            return Color.rgb(128, 0, 128)
        if v == "red":
            return Color.rgb(255, 0, 0)
        if v == "rosybrown":
            return Color.rgb(188, 143, 143)
        if v == "royalblue":
            return Color.rgb(65, 105, 225)
        if v == "saddlebrown":
            return Color.rgb(139, 69, 19)
        if v == "salmon":
            return Color.rgb(250, 128, 114)
        if v == "sandybrown":
            return Color.rgb(244, 164, 96)
        if v == "seagreen":
            return Color.rgb(46, 139, 87)
        if v == "seashell":
            return Color.rgb(255, 245, 238)
        if v == "sienna":
            return Color.rgb(160, 82, 45)
        if v == "silver":
            return Color.rgb(192, 192, 192)
        if v == "skyblue":
            return Color.rgb(135, 206, 235)
        if v == "slateblue":
            return Color.rgb(106, 90, 205)
        if v == "slategray":
            return Color.rgb(112, 128, 144)
        if v == "slategrey":
            return Color.rgb(112, 128, 144)
        if v == "snow":
            return Color.rgb(255, 250, 250)
        if v == "springgreen":
            return Color.rgb(0, 255, 127)
        if v == "steelblue":
            return Color.rgb(70, 130, 180)
        if v == "tan":
            return Color.rgb(210, 180, 140)
        if v == "teal":
            return Color.rgb(0, 128, 128)
        if v == "thistle":
            return Color.rgb(216, 191, 216)
        if v == "tomato":
            return Color.rgb(255, 99, 71)
        if v == "turquoise":
            return Color.rgb(64, 224, 208)
        if v == "violet":
            return Color.rgb(238, 130, 238)
        if v == "wheat":
            return Color.rgb(245, 222, 179)
        if v == "white":
            return Color.rgb(255, 255, 255)
        if v == "whitesmoke":
            return Color.rgb(245, 245, 245)
        if v == "yellow":
            return Color.rgb(255, 255, 0)
        if v == "yellowgreen":
            return Color.rgb(154, 205, 50)
        return Color.rgb(0, 0, 0)

    @classmethod
    def parse_color_hex(cls, hex_string):
        """Parse SVG Color by Hex String"""
        h = hex_string.lstrip('#')
        size = len(h)
        if size == 8:
            return cls(int(h[:8], 16))
        elif size == 6:
            return cls(int(h[:6], 16))
        elif size == 4:
            return cls(int(h[3] + h[3] + h[2] + h[2] + h[1] + h[1] + h[0] + h[0], 16))
        elif size == 3:
            return cls(int(h[2] + h[2] + h[1] + h[1] + h[0] + h[0], 16))
        return Color.rgb(0, 0, 0)

    @classmethod
    def parse_color_rgb(cls, values):
        """Parse SVG Color, RGB value declarations """
        int_values = list(map(int, values))
        return Color.rgb(int_values[0], int_values[1], int_values[2])

    @classmethod
    def parse_color_rgbp(cls, values):
        """Parse SVG color, RGB percent value declarations"""
        ratio = 255.0 / 100.0
        values = list(map(float, values))
        return Color.rgb(int(values[0] * ratio), int(values[1] * ratio), int(values[2] * ratio))

    @property
    def alpha(self):
        return (self >> 24) & 0xFF

    @property
    def red(self):
        return (self >> 16) & 0xFF

    @property
    def green(self):
        return (self >> 8) & 0xFF

    @property
    def blue(self):
        return self & 0xFF

    @property
    def hex(self):
        return '#%02x%02x%02x' % (self.red, self.green, self.blue)


def segment_length(curve, start, end, start_point, end_point, error, min_depth, depth):
    """Recursively approximates the length by straight lines"""
    mid = (start + end) / 2
    mid_point = curve.point(mid)
    length = abs(end_point - start_point)
    first_half = abs(mid_point - start_point)
    second_half = abs(end_point - mid_point)

    length2 = first_half + second_half
    if (length2 - length > error) or (depth < min_depth):
        # Calculate the length of each segment:
        depth += 1
        return (segment_length(curve, start, mid, start_point, mid_point,
                               error, min_depth, depth) +
                segment_length(curve, mid, end, mid_point, end_point,
                               error, min_depth, depth))
    # This is accurate enough.
    return length2


# Path and Relevant Subobjects

class Point:
    """Point is a general subscriptable point class with .x and .y as well as [0] and [1]

    For compatibility with regebro svg.path we accept complex numbers as points x + yj,
    and provide .real and .imag as properties. As well as float and integer values as (v,0) elements.

    With regard to SGV 7.15.1 defining SVGPoint this class provides for matrix transformations.
    """

    def __init__(self, x, y=None):
        if x is not None and y is None:
            if isinstance(x, str):
                string_x, string_y = REGEX_COORD_PAIR.findall(x)[0]
                x = float(string_x)
                y = float(string_y)
            else:
                try:  # try subscription.
                    y = x[1]
                    x = x[0]
                except TypeError:
                    try:  # Try .x .y
                        y = x.y
                        x = x.x
                    except AttributeError:
                        try:  # try .imag .real complex values.
                            y = x.imag
                            x = x.real
                        except AttributeError:
                            # Unknown.
                            x = 0
                            y = 0
        self.x = x
        self.y = y

    def __key(self):
        return (self.x, self.y)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        a0 = self[0]
        a1 = self[1]
        if isinstance(other, str):
            other = Point(other)
        if isinstance(other, (Point, list, tuple)):
            b0 = other[0]
            b1 = other[1]
        elif isinstance(other, complex):
            b0 = other.real
            b1 = other.imag
        else:
            return NotImplemented
        try:
            c0 = abs(a0 - b0) <= ERROR
            c1 = abs(a1 - b1) <= ERROR
        except TypeError:
            return False
        return c0 and c1

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        else:
            raise IndexError

    def __repr__(self):
        x_str = ('%.12f' % (self.x))
        if '.' in x_str:
            x_str = x_str.rstrip('0').rstrip('.')
        y_str = ('%.12f' % (self.y))
        if '.' in y_str:
            y_str = y_str.rstrip('0').rstrip('.')
        return "Point(%s,%s)" % (x_str, y_str)

    def __copy__(self):
        return Point(self.x, self.y)

    def __str__(self):
        x_str = ('%G' % (self.x))
        if '.' in x_str:
            x_str = x_str.rstrip('0').rstrip('.')
        y_str = ('%G' % (self.y))
        if '.' in y_str:
            y_str = y_str.rstrip('0').rstrip('.')
        return "%s,%s" % (x_str, y_str)

    def __imul__(self, other):
        if isinstance(other, Matrix):
            v = other.point_in_matrix_space(self)
            self[0] = v[0]
            self[1] = v[1]
        elif isinstance(other, (int, float)):  # Emulates complex point multiplication by real.
            self.x *= other
            self.y *= other
        else:
            return NotImplemented
        return self

    def __mul__(self, other):
        if isinstance(other, (Matrix, int, float)):
            n = copy(self)
            n *= other
            return n

    __rmul__ = __mul__

    def __iadd__(self, other):
        if isinstance(other, (Point, tuple, list)):
            self[0] += other[0]
            self[1] += other[1]
        elif isinstance(other, complex):
            self[0] += other.real
            self[1] += other.imag
        elif isinstance(other, (float, int)):
            self[0] += other
        else:
            return NotImplemented
        return self

    def __add__(self, other):
        if isinstance(other, (Point, tuple, list, complex, int, float)):
            n = copy(self)
            n += other
            return n

    __radd__ = __add__

    def __isub__(self, other):
        if isinstance(other, (Point, tuple, list)):
            self[0] -= other[0]
            self[1] -= other[1]
        elif isinstance(other, complex):
            self[0] -= other.real
            self[1] -= other.imag
        elif isinstance(other, (float, int)):
            self[0] -= other
        else:
            return NotImplemented
        return self

    def __sub__(self, other):
        if isinstance(other, (Point, tuple, list, complex, int, float)):
            n = copy(self)
            n -= other
            return n

    def __rsub__(self, other):
        if isinstance(other, (Point, tuple, list)):
            x = other[0] - self[0]
            y = other[1] - self[1]
        elif isinstance(other, complex):
            x = other.real - self[0]
            y = other.imag - self[1]
        elif isinstance(other, (float, int)):
            x = other - self[0]
            y = self[1]
        else:
            return NotImplemented
        return Point(x, y)

    def __abs__(self):
        return hypot(self.x, self.y)

    def __pow__(self, other):
        r_raised = abs(self) ** other
        argz_multiplied = self.argz() * other

        real_part = round(r_raised * cos(argz_multiplied))
        imag_part = round(r_raised * sin(argz_multiplied))
        return self.__class__(real_part, imag_part)

    def conjugate(self):
        return self.__class__(self.real, -self.imag)

    def argz(self):
        return atan(self.imag / self.real)

    @property
    def real(self):
        """Emulate svg.path use of complex numbers"""
        return self.x

    @property
    def imag(self):
        """Emulate svg.path use of complex numbers"""
        return self.y

    def matrix_transform(self, matrix):
        v = matrix.point_in_matrix_space(self)
        self[0] = v[0]
        self[1] = v[1]
        return self

    def move_towards(self, p2, amount=1):
        self.x = amount * (p2[0] - self[0]) + self[0]
        self.y = amount * (p2[1] - self[1]) + self[1]

    def distance_to(self, p2):
        return Point.distance(self, p2)

    def angle_to(self, p2):
        return Point.angle(self, p2)

    def polar_to(self, angle, distance):
        return Point.polar(self, angle, distance)

    def reflected_across(self, p):
        m = p + p
        m -= self
        return m

    @staticmethod
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0
        elif val > 0:
            return 1
        else:
            return 2

    @staticmethod
    def convex_hull(pts):
        if len(pts) == 0:
            return
        points = sorted(set(pts), key=lambda p: p[0])
        first_point_on_hull = points[0]
        point_on_hull = first_point_on_hull
        while True:
            yield point_on_hull
            endpoint = point_on_hull
            for t in points:
                if point_on_hull is endpoint \
                        or Point.orientation(point_on_hull, t, endpoint) == 2:
                    endpoint = t
            point_on_hull = endpoint
            if first_point_on_hull is point_on_hull:
                break

    @staticmethod
    def distance(p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        dx *= dx
        dy *= dy
        return sqrt(dx + dy)

    @staticmethod
    def polar(p1, angle, r):
        dx = cos(angle) * r
        dy = sin(angle) * r
        return Point(p1[0] + dx, p1[1] + dy)

    @staticmethod
    def angle(p1, p2):
        return Angle.radians(atan2(p2[1] - p1[1], p2[0] - p1[0]))

    @staticmethod
    def towards(p1, p2, amount):
        tx = amount * (p2[0] - p1[0]) + p1[0]
        ty = amount * (p2[1] - p1[1]) + p1[1]
        return Point(tx, ty)


class Angle(float):
    """CSS Angle defines as used in SVG"""

    def __repr__(self):
        return "Angle(%.12f)" % self

    def __copy__(self):
        return Angle(self)

    def __eq__(self, other):
        # Python 2
        c1 = abs(self - other) <= 1e-11
        return c1

    @classmethod
    def parse(cls, angle_string):
        if not isinstance(angle_string, str):
            return
        angle_string = angle_string.lower()
        if angle_string.endswith('deg'):
            return Angle.degrees(float(angle_string[:-3]))
        if angle_string.endswith('grad'):
            return Angle.gradians(float(angle_string[:-4]))
        if angle_string.endswith('rad'):  # Must be after 'grad' since 'grad' ends with 'rad' too.
            return Angle.radians(float(angle_string[:-3]))
        if angle_string.endswith('turn'):
            return Angle.turns(float(angle_string[:-4]))
        return Angle.degrees(float(angle_string))

    @classmethod
    def radians(cls, radians):
        return cls(radians)

    @classmethod
    def degrees(cls, degrees):
        return cls(tau * degrees / 360.0)

    @classmethod
    def gradians(cls, gradians):
        return cls(tau * gradians / 400.0)

    @classmethod
    def turns(cls, turns):
        return cls(tau * turns)

    @property
    def as_radians(self):
        return self

    @property
    def as_degrees(self):
        return self * 360.0 / tau

    @property
    def as_positive_degrees(self):
        v = self * 360.0 / tau
        while v < 0:
            v += 360.0
        return v

    @property
    def as_gradians(self):
        return self * 400.0 / tau

    @property
    def as_turns(self):
        return self / tau


class Matrix:
    """"
    Provides svg matrix interfacing.

    SVG 7.15.3 defines the matrix form as:
    [a c  e]
    [b d  f]
    """

    def __init__(self, *components):
        self.a = 1.0
        self.b = 0.0
        self.c = 0.0
        self.d = 1.0
        self.e = 0.0
        self.f = 0.0
        len_args = len(components)
        if len_args == 0:
            pass
        elif len_args == 1:
            m = components[0]
            if isinstance(m, str):
                self.parse(m)
            else:
                self.a = m[0]
                self.b = m[1]
                self.c = m[2]
                self.d = m[3]
                self.e = m[4]
                self.f = m[5]
        else:
            self.a = components[0]
            self.b = components[1]
            self.c = components[2]
            self.d = components[3]
            self.e = components[4]
            self.f = components[5]

    def __ne__(self, other):
        return other is None or \
               not isinstance(other, Matrix) or \
               self.a != other.a or self.b != other.b or \
               self.c != other.c or self.d != other.d or \
               self.e != other.e or self.f != other.f

    def __eq__(self, other):
        return not self.__ne__(other)

    def __len__(self):
        return 6

    def __matmul__(self, other):
        m = copy(self)
        m.__imatmul__(other)
        return m

    def __rmatmul__(self, other):
        m = copy(other)
        m.__imatmul__(self)
        return m

    def __imatmul__(self, other):
        self.a, self.b, self.c, self.d, self.e, self.f = Matrix.matrix_multiply(self, other)
        return self

    __mul__ = __matmul__
    __rmul__ = __rmatmul__
    __imul__ = __imatmul__

    def __getitem__(self, item):
        if item == 0:
            return self.a
        elif item == 1:
            return self.b
        elif item == 2:
            return self.c
        elif item == 3:
            return self.d
        elif item == 4:
            return self.e
        elif item == 5:
            return self.f

    def __setitem__(self, key, value):
        if key == 0:
            self.a = value
        elif key == 1:
            self.b = value
        elif key == 2:
            self.c = value
        elif key == 3:
            self.d = value
        elif key == 4:
            self.e = value
        elif key == 5:
            self.f = value

    def __repr__(self):
        return "Matrix(%3f, %3f, %3f, %3f, %3f, %3f)" % \
               (self.a, self.b, self.c, self.d, self.e, self.f)

    def __copy__(self):
        return Matrix(self.a, self.b, self.c, self.d, self.e, self.f)

    def __str__(self):
        """
        Many of SVG's graphics operations utilize 2x3 matrices of the form:

        :returns string representation of matrix.
        """
        return "[%3f, %3f,\n %3f, %3f,   %3f, %3f]" % \
               (self.a, self.c, self.b, self.d, self.e, self.f)

    def parse(self, transform_str):
        """Parses the svg transform string.

        Transforms from SVG 1.1 have a smaller complete set of operations. Whereas in SVG 2.0 they gain
        the CSS transforms and the additional functions and parsing that go with that. This parse is
        compatible with SVG 1.1 and the SVG 2.0 which includes the CSS 2d superset.

        CSS transforms have scalex() scaley() translatex(), translatey(), and skew() (deprecated).
        2D CSS angles haves units: "deg" tau / 360, "rad" tau/tau, "grad" tau/400, "turn" tau.
        2D CSS distances have length/percentages: "px", "cm", "mm", "in", "pt", etc. (+|-)?d+%"""
        if not transform_str:
            return
        if not isinstance(transform_str, str):
            raise TypeError('Must provide a string to parse')

        for sub_element in REGEX_TRANSFORM_TEMPLATE.findall(transform_str.lower()):
            name = sub_element[0]
            params = tuple(REGEX_TRANSFORM_PARAMETER.findall(sub_element[1]))
            params = [mag + units for mag, units in params]
            if SVG_TRANSFORM_MATRIX == name:
                params = map(float, params)
                self.pre_cat(*params)
            elif SVG_TRANSFORM_TRANSLATE == name:
                params = map(Distance.parse, params)
                self.pre_translate(*params)
            elif SVG_TRANSFORM_TRANSLATE_X == name:
                self.pre_translate(Distance.parse(params[0]), 0)
            elif SVG_TRANSFORM_TRANSLATE_Y == name:
                self.pre_translate(0, Distance.parse(params[0]))
            elif SVG_TRANSFORM_SCALE == name:
                params = map(float, params)
                self.pre_scale(*params)
            elif SVG_TRANSFORM_SCALE_X == name:
                self.pre_scale(float(params[0]), 1)
            elif SVG_TRANSFORM_SCALE_Y == name:
                self.pre_scale(1, float(params[0]))
            elif SVG_TRANSFORM_ROTATE == name:
                angle = Angle.parse(params[0])
                params = map(Distance.parse, params[1:])
                self.pre_rotate(angle, *params)
            elif SVG_TRANSFORM_SKEW == name:
                angle_a = Angle.parse(params[0])
                angle_b = Angle.parse(params[1])
                params = map(Distance.parse, params[2:])
                self.pre_skew(angle_a, angle_b, *params)
            elif SVG_TRANSFORM_SKEW_X == name:
                angle_a = Angle.parse(params[0])
                params = map(Distance.parse, params[1:])
                self.pre_skew_x(angle_a, *params)
            elif SVG_TRANSFORM_SKEW_Y == name:
                angle_b = Angle.parse(params[0])
                params = map(Distance.parse, params[1:])
                self.pre_skew_y(angle_b, *params)
        return self

    def value_trans_x(self):
        return self.e

    def value_trans_y(self):
        return self.f

    def value_scale_x(self):
        return self.a

    def value_scale_y(self):
        return self.d

    def value_skew_x(self):
        return self.b

    def value_skew_y(self):
        return self.c

    def reset(self):
        """Resets matrix to identity."""
        self.a = 1.0
        self.b = 0.0
        self.c = 0.0
        self.d = 1.0

        self.e = 0.0
        self.f = 0.0

    def inverse(self):
        """
        [a c e]
        [b d f]
        """
        m48s75 = self.d * 1 - self.f * 0
        m38s56 = 0 * self.e - self.c * 1
        m37s46 = self.c * self.f - self.d * self.e
        det = self.a * m48s75 + self.c * m38s56 + 0 * m37s46
        inverse_det = 1.0 / float(det)

        self.a = m48s75 * inverse_det
        self.b = (0 * self.f - self.c * 1) * inverse_det
        # self.g = (self.c * self.h - self.g * self.d) * inverse_det
        self.c = m38s56 * inverse_det
        self.d = (self.a * 1 - 0 * self.e) * inverse_det
        # self.h = (self.c * self.g - self.a * self.h) * inverse_det
        self.e = m37s46 * inverse_det
        self.f = (0 * self.c - self.a * self.f) * inverse_det
        # self.i = (self.a * self.d - self.c * self.c) * inverse_det

    def post_cat(self, *components):
        mx = Matrix(*components)
        self.__imatmul__(mx)

    def post_scale(self, sx=1.0, sy=None, x=0.0, y=0.0):
        if sy is None:
            sy = sx
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if x == 0 and y == 0:
            self.post_cat(Matrix.scale(sx, sy))
        else:
            self.post_translate(-x, -y)
            self.post_scale(sx, sy)
            self.post_translate(x, y)

    def post_scale_x(self, sx=1.0, x=0.0, y=0.0):
        self.post_scale(sx, 1, x, y)

    def post_scale_y(self, sy=1.0, x=0.0, y=0.0):
        self.post_scale(1, sy, x, y)

    def post_translate(self, tx=0.0, ty=0.0):
        self.post_cat(Matrix.translate(tx, ty))

    def post_translate_x(self, tx=0.0):
        self.post_translate(tx, 0.0)

    def post_translate_y(self, ty=0.0):
        self.post_translate(0.0, ty)

    def post_rotate(self, angle, x=0.0, y=0.0):
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if x == 0 and y == 0:
            self.post_cat(Matrix.rotate(angle))  # self %= self.get_rotate(theta)
        else:
            matrix = Matrix()
            matrix.post_translate(-x, -y)
            matrix.post_cat(Matrix.rotate(angle))
            matrix.post_translate(x, y)
            self.post_cat(matrix)

    def post_skew(self, angle_a=0.0, angle_b=0.0, x=0.0, y=0.0):
        if x is None:
            x = 0
        if y is None:
            y = 0
        if x == 0 and y == 0:
            self.post_cat(Matrix.skew(angle_a, angle_b))
        else:
            self.post_translate(-x, -y)
            self.post_skew(angle_a, angle_b)
            self.post_translate(x, y)

    def post_skew_x(self, angle_a=0.0, x=0.0, y=0.0):
        self.post_skew(angle_a, 0.0, x, y)

    def post_skew_y(self, angle_b=0.0, x=0.0, y=0.0):
        self.post_skew(0.0, angle_b, x, y)

    def pre_cat(self, *components):
        mx = Matrix(*components)
        self.a, self.b, self.c, self.d, self.e, self.f = Matrix.matrix_multiply(mx, self)

    def pre_scale(self, sx=1.0, sy=None, x=0.0, y=0.0):
        if sy is None:
            sy = sx
        if x is None:
            x = 0.0
        if y is None:
            y = 0.0
        if x == 0 and y == 0:
            self.pre_cat(Matrix.scale(sx, sy))
        else:
            self.pre_translate(x, y)
            self.pre_scale(sx, sy)
            self.pre_translate(-x, -y)

    def pre_scale_x(self, sx=1.0, x=0.0, y=0.0):
        self.pre_scale(sx, 1, x, y)

    def pre_scale_y(self, sy=1.0, x=0.0, y=0.0):
        self.pre_scale(1, sy, x, y)

    def pre_translate(self, tx=0.0, ty=0.0):
        self.pre_cat(Matrix.translate(tx, ty))

    def pre_translate_x(self, tx=0.0):
        self.pre_translate(tx, 0.0)

    def pre_translate_y(self, ty=0.0):
        self.pre_translate(0.0, ty)

    def pre_rotate(self, angle, x=0.0, y=0.0):
        if x is None:
            x = 0
        if y is None:
            y = 0
        if x == 0 and y == 0:
            self.pre_cat(Matrix.rotate(angle))
        else:
            self.pre_translate(x, y)
            self.pre_rotate(angle)
            self.pre_translate(-x, -y)

    def pre_skew(self, angle_a=0.0, angle_b=0.0, x=0.0, y=0.0):
        if x is None:
            x = 0
        if y is None:
            y = 0
        if x == 0 and y == 0:
            self.pre_cat(Matrix.skew(angle_a, angle_b))
        else:
            self.pre_translate(x, y)
            self.pre_skew(angle_a, angle_b)
            self.pre_translate(-x, -y)

    def pre_skew_x(self, angle_a=0.0, x=0.0, y=0.0):
        self.pre_skew(angle_a, 0, x, y)

    def pre_skew_y(self, angle_b=0.0, x=0.0, y=0.0):
        self.pre_skew(0.0, angle_b, x, y)

    def point_in_inverse_space(self, v0):
        inverse = Matrix(self)
        inverse.inverse()
        return inverse.point_in_matrix_space(v0)

    def point_in_matrix_space(self, v0):
        return Point(v0[0] * self.a + v0[1] * self.c + 1 * self.e,
                     v0[0] * self.b + v0[1] * self.d + 1 * self.f)

    def transform_point(self, v):
        nx = v[0] * self.a + v[1] * self.c + 1 * self.e
        ny = v[0] * self.b + v[1] * self.d + 1 * self.f
        v[0] = nx
        v[1] = ny

    @classmethod
    def scale(cls, sx=1.0, sy=None):
        if sy is None:
            sy = sx
        return cls(sx, 0,
                   0, sy, 0, 0)

    @classmethod
    def scale_x(cls, sx=1.0):
        return cls.scale(sx, 1.0)

    @classmethod
    def scale_y(cls, sy=1.0):
        return cls.scale(1.0, sy)

    @classmethod
    def translate(cls, tx=0.0, ty=0.0):
        """SVG Matrix:
                [a c e]
                [b d f]
                """
        return cls(1.0, 0.0,
                   0.0, 1.0, tx, ty)

    @classmethod
    def translate_x(cls, tx=0.0):
        return cls.translate(tx, 0)

    @classmethod
    def translate_y(cls, ty=0.0):
        return cls.translate(0.0, ty)

    @classmethod
    def rotate(cls, angle=0.0):
        ct = cos(angle)
        st = sin(angle)
        return cls(ct, st,
                   -st, ct, 0.0, 0.0)

    @classmethod
    def skew(cls, angle_a=0.0, angle_b=0.0):
        aa = tan(angle_a)
        bb = tan(angle_b)
        return cls(1.0, bb,
                   aa, 1.0, 0.0, 0.0)

    @classmethod
    def skew_x(cls, angle=0.0):
        return cls.skew(angle, 0.0)

    @classmethod
    def skew_y(cls, angle=0.0):
        return cls.skew(0.0, angle)

    @classmethod
    def identity(cls):
        """
        1, 0, 0,
        0, 1, 0,
        """
        return cls()

    @staticmethod
    def matrix_multiply(m, s):
        """
        [a c e]      [a c e]   [a b 0]
        [b d f]   %  [b d f] = [c d 0]
        [0 0 1]      [0 0 1]   [e f 1]

        :param m0: matrix operand
        :param m1: matrix operand
        :return: muliplied matrix.
        """
        r0 = s.a * m.a + s.c * m.b + s.e * 0, \
             s.a * m.c + s.c * m.d + s.e * 0, \
             s.a * m.e + s.c * m.f + s.e * 1

        r1 = s.b * m.a + s.d * m.b + s.f * 0, \
             s.b * m.c + s.d * m.d + s.f * 0, \
             s.b * m.e + s.d * m.f + s.f * 1

        return r0[0], r1[0], r0[1], r1[1], r0[2], r1[2]


class PathSegment:
    """This is the base class for all the segment within a path."""

    def __init__(self):
        self.start = None
        self.end = None

    def __mul__(self, other):
        if isinstance(other, Matrix):
            n = copy(self)
            n *= other
            return n
        elif isinstance(other, str):
            n = copy(self)
            n *= Matrix(other)
            return n
        return NotImplemented

    __rmul__ = __mul__

    def __iadd__(self, other):
        if isinstance(other, PathSegment):
            path = Path(self, other)
            return path
        elif isinstance(other, str):
            path = Path(self) + other
            return path
        return NotImplemented

    __add__ = __iadd__

    def __str__(self):
        return self.d()

    def __iter__(self):
        self.n = -1
        return self

    def __next__(self):
        self.n += 1
        try:
            val = self[self.n]
            if val is None:
                self.n += 1
                val = self[self.n]
            return val
        except IndexError:
            raise StopIteration

    next = __next__

    def plot(self):
        pass

    def bbox(self):
        """returns the bounding box for the segment.
        xmin, ymin, xmax, ymax
        """
        xs = [p[0] for p in self if p is not None]
        ys = [p[1] for p in self if p is not None]
        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)
        return xmin, ymin, xmax, ymax

    def reverse(self):
        end = self.end
        self.end = self.start
        self.start = end

    def point(self, t):
        return self.end

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        return 0

    def d(self, current_point=None, smooth=False):
        """If current point is None, the function will return the absolute form. If it contains a point,
        it will give the value relative to that point."""
        raise NotImplementedError


class Move(PathSegment):
    """Represents move commands. Does nothing, but is there to handle
    paths that consist of only move commands, which is valid, but pointless.
    Also serve as a bridge to make discontinuous paths into continuous paths
    with non-drawn sections.
    """

    def __init__(self, *args, **kwargs):
        """
        Move commands most importantly go to a place. So if one location is given, that's the end point.
        If two locations are given then first is the start location.

        Move(p) where p is the End point.
        Move(s,e) where s is the Start point, e is the End point.
        Move(p, start=s) where p is End point, s is the Start point.
        Move(p, end=e) where p is the Start point, e is the End point.
        Move(start=s, end=e) where s is the Start point, e is the End point.
        """
        PathSegment.__init__(self)
        self.end = None
        self.start = None
        if len(args) == 0:
            if 'end' in kwargs:
                self.end = kwargs['end']
            if 'start' in kwargs:
                self.start = kwargs['start']
        elif len(args) == 1:
            if len(kwargs) == 0:
                self.end = args[0]
            else:
                if 'end' in kwargs:
                    self.start = args[0]
                    self.end = kwargs['end']
                elif 'start' in kwargs:
                    self.start = kwargs['start']
                    self.end = args[0]
        elif len(args) == 2:
            self.start = args[0]
            self.end = args[1]
        if self.start is not None:
            self.start = Point(self.start)
        if self.end is not None:
            self.end = Point(self.end)

    def __imul__(self, other):
        if isinstance(other, Matrix):
            if self.start is not None:
                self.start *= other
            if self.end is not None:
                self.end *= other
        return self

    def __repr__(self):
        if self.start is None:
            return 'Move(end=%s)' % repr(self.end)
        else:
            return 'Move(start=%s, end=%s)' % (repr(self.start), repr(self.end))

    def __copy__(self):
        return Move(self.start, self.end)

    def __eq__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        if not isinstance(other, Move):
            return NotImplemented
        return not self == other

    def __len__(self):
        return 2

    def __getitem__(self, item):
        if item == 0:
            return self.start
        elif item == 1:
            return self.end
        else:
            raise IndexError

    def plot(self):
        if self.start is not None:
            for x, y in Line.plot_line(self.start[0], self.start[1], self.end[0], self.end[1]):
                yield x, y, 0

    def d(self, current_point=None, smooth=False):
        if current_point is None:
            return 'M %s' % (self.end)
        else:
            return 'm %s' % (self.end - current_point)


class Close(PathSegment):
    """Represents close commands. If this exists at the end of the shape then the shape is closed.
    the methodology of a single flag close fails in a couple ways. You can have multi-part shapes
    which can close or not close several times.
    """

    def __init__(self, start=None, end=None):
        PathSegment.__init__(self)
        self.end = None
        self.start = None
        if start is not None:
            self.start = Point(start)
        if end is not None:
            self.end = Point(end)

    def __imul__(self, other):
        if isinstance(other, Matrix):
            if self.start is not None:
                self.start *= other
            if self.end is not None:
                self.end *= other
        return self

    def __repr__(self):
        if self.start is None and self.end is None:
            return 'Close()'
        s = self.start
        if s is not None:
            s = repr(s)
        e = self.end
        if e is not None:
            e = repr(e)
        return 'Close(start=%s, end=%s)' % (s, e)

    def __copy__(self):
        return Close(self.start, self.end)

    def __eq__(self, other):
        if not isinstance(other, Close):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        if not isinstance(other, Close):
            return NotImplemented
        return not self == other

    def __len__(self):
        return 2

    def __getitem__(self, item):
        if item == 0:
            return self.start
        elif item == 1:
            return self.end
        else:
            raise IndexError

    def plot(self):
        if self.start is not None and self.end is not None:
            for x, y in Line.plot_line(self.start[0], self.start[1], self.end[0], self.end[1]):
                yield x, y, 1

    def length(self, error=None, min_depth=None):
        if self.start is not None and self.end is not None:
            return Point.distance(self.end, self.start)
        else:
            return 0

    def d(self, current_point=None, smooth=False):
        if current_point is None:
            return 'Z'
        else:
            return 'z'


class Line(PathSegment):
    def __init__(self, start, end):
        PathSegment.__init__(self)
        self.end = None
        self.start = None
        if start is not None:
            self.start = Point(start)
        if end is not None:
            self.end = Point(end)

    def __repr__(self):
        if self.start is None:
            return 'Line(end=%s)' % (repr(self.end))
        return 'Line(start=%s, end=%s)' % (repr(self.start), repr(self.end))

    def __copy__(self):
        return Line(self.start, self.end)

    def __eq__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return self.start == other.start and self.end == other.end

    def __ne__(self, other):
        if not isinstance(other, Line):
            return NotImplemented
        return not self == other

    def __imul__(self, other):
        if isinstance(other, Matrix):
            if self.start is not None:
                self.start *= other
            if self.end is not None:
                self.end *= other
        return self

    def __len__(self):
        return 2

    def __getitem__(self, item):
        if item == 0:
            return self.start
        elif item == 1:
            return self.end
        else:
            raise IndexError

    def point(self, t):
        return Point.towards(self.start, self.end, t)

    def length(self, error=None, min_depth=None):
        return Point.distance(self.end, self.start)

    def closest_segment_point(self, p, respect_bounds=True):
        """ Gives the t value of the point on the line closest to the given point. """
        a = self.start
        b = self.end
        vAPx = p[0] - a[0]
        vAPy = p[1] - a[1]
        vABx = b[0] - a[0]
        vABy = b[1] - a[1]
        sqDistanceAB = vABx * vABx + vABy * vABy
        ABAPproduct = vABx * vAPx + vABy * vAPy
        if sqDistanceAB == 0:
            return 0  # Line is point.
        amount = ABAPproduct / sqDistanceAB
        if respect_bounds:
            if amount > 1:
                amount = 1
            if amount < 0:
                amount = 0
        return self.point(amount)

    def d(self, current_point=None, smooth=False):
        if current_point is None:
            return 'L %s' % (self.end)
        else:
            return 'l %s' % (self.end - current_point)

    def plot(self):
        for x, y in Line.plot_line(self.start[0], self.start[1], self.end[0], self.end[1]):
            yield x, y, 1

    @staticmethod
    def plot_line(x0, y0, x1, y1):
        """Zingl-Bresenham line draw algorithm"""
        x0 = int(x0)
        y0 = int(y0)
        x1 = int(x1)
        y1 = int(y1)
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)

        if x0 < x1:
            sx = 1
        else:
            sx = -1
        if y0 < y1:
            sy = 1
        else:
            sy = -1

        err = dx + dy  # error value e_xy

        while True:  # /* loop */
            yield x0, y0
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:  # e_xy+e_y < 0
                err += dy
                x0 += sx
            if e2 <= dx:  # e_xy+e_y < 0
                err += dx
                y0 += sy


class QuadraticBezier(PathSegment):
    def __init__(self, start, control, end):
        PathSegment.__init__(self)
        self.end = None
        self.control = None
        self.start = None
        if start is not None:
            self.start = Point(start)
        if control is not None:
            self.control = Point(control)
        if end is not None:
            self.end = Point(end)

    def __repr__(self):
        return 'QuadraticBezier(start=%s, control=%s, end=%s)' % (
            repr(self.start), repr(self.control), repr(self.end))

    def __copy__(self):
        return QuadraticBezier(self.start, self.control, self.end)

    def __eq__(self, other):
        if not isinstance(other, QuadraticBezier):
            return NotImplemented
        return self.start == other.start and self.end == other.end and \
               self.control == other.control

    def __ne__(self, other):
        if not isinstance(other, QuadraticBezier):
            return NotImplemented
        return not self == other

    def __imul__(self, other):
        if isinstance(other, Matrix):
            if self.start is not None:
                self.start *= other
            if self.control is not None:
                self.control *= other
            if self.end is not None:
                self.end *= other
        return self

    def __len__(self):
        return 3

    def __getitem__(self, item):
        if item == 0:
            return self.start
        elif item == 1:
            return self.control
        elif item == 2:
            return self.end
        raise IndexError

    def point(self, t):
        """Calculate the x,y position at a certain position of the path"""
        x0, y0 = self.start
        x1, y1 = self.control
        x2, y2 = self.end
        x = (1 - t) * (1 - t) * x0 + 2 * (1 - t) * t * x1 + t * t * x2
        y = (1 - t) * (1 - t) * y0 + 2 * (1 - t) * t * y1 + t * t * y2
        return Point(x, y)

    def length(self, error=None, min_depth=None):
        """Calculate the length of the path up to a certain position"""
        a = self.start - 2 * self.control + self.end
        b = 2 * (self.control - self.start)
        a_dot_b = a.real * b.real + a.imag * b.imag

        if abs(a) < 1e-12:
            s = abs(b)
        elif abs(a_dot_b + abs(a) * abs(b)) < 1e-12:
            k = abs(b) / abs(a)
            if k >= 2:
                s = abs(b) - abs(a)
            else:
                s = abs(a) * (k ** 2 / 2 - k + 1)
        else:
            # For an explanation of this case, see
            # http://www.malczak.info/blog/quadratic-bezier-curve-length/
            A = 4 * (a.real ** 2 + a.imag ** 2)
            B = 4 * (a.real * b.real + a.imag * b.imag)
            C = b.real ** 2 + b.imag ** 2

            Sabc = 2 * sqrt(A + B + C)
            A2 = sqrt(A)
            A32 = 2 * A * A2
            C2 = 2 * sqrt(C)
            BA = B / A2

            s = (A32 * Sabc + A2 * B * (Sabc - C2) + (4 * C * A - B ** 2) *
                 log((2 * A2 + BA + Sabc) / (BA + C2))) / (4 * A32)
        return s

    def is_smooth_from(self, previous):
        """Checks if this segment would be a smooth segment following the previous"""
        if isinstance(previous, QuadraticBezier):
            return (self.start == previous.end and
                    (self.control - self.start) == (previous.end - previous.control))
        else:
            return self.control == self.start

    def d(self, current_point=None, smooth=False):
        if smooth:
            if current_point is None:
                return 'T %s' % (self.end)
            else:
                return 't %s' % (self.end - current_point)
        else:
            if current_point is None:
                return 'Q %s %s' % (self.control, self.end)
            else:
                return 'q %s %s' % (self.control - current_point, self.end - current_point)

    def plot(self):
        for x, y in QuadraticBezier.plot_quad_bezier(self.start[0], self.start[1],
                                                     self.control[0], self.control[1],
                                                     self.end[0], self.end[1]):
            yield x, y, 1

    @staticmethod
    def plot_quad_bezier_seg(x0, y0, x1, y1, x2, y2):
        """plot a limited quadratic Bezier segment
        This algorithm can plot curves that do not inflect.
        It is used as part of the general algorithm, which breaks at the infection points"""
        sx = x2 - x1
        sy = y2 - y1
        xx = x0 - x1
        yy = y0 - y1
        xy = 0  # relative values for checks */
        dx = 0
        dy = 0
        err = 0
        cur = xx * sy - yy * sx  # /* curvature */
        points = None

        assert (xx * sx <= 0 and yy * sy <= 0)  # /* sign of gradient must not change */

        if sx * sx + sy * sy > xx * xx + yy * yy:  # /* begin with shorter part */
            x2 = x0
            x0 = sx + x1
            y2 = y0
            y0 = sy + y1
            cur = -cur  # /* swap P0 P2 */
            points = []
        if cur != 0:  # /* no straight line */
            xx += sx
            if x0 < x2:
                sx = 1  # /* x step direction */
            else:
                sx = -1  # /* x step direction */
            xx *= sx
            yy += sy
            if y0 < y2:
                sy = 1
            else:
                sy = -1
            yy *= sy  # /* y step direction */
            xy = 2 * xx * yy
            xx *= xx
            yy *= yy  # /* differences 2nd degree */
            if cur * sx * sy < 0:  # /* negated curvature? */
                xx = -xx
                yy = -yy
                xy = -xy
                cur = -cur
            dx = 4.0 * sy * cur * (x1 - x0) + xx - xy  # /* differences 1st degree */
            dy = 4.0 * sx * cur * (y0 - y1) + yy - xy
            xx += xx
            yy += yy
            err = dx + dy + xy  # /* error 1st step */
            while True:
                if points is None:
                    yield x0, y0  # /* plot curve */
                else:
                    points.append((x0, y0))
                if x0 == x2 and y0 == y2:
                    if points is not None:
                        for plot in reversed(points):
                            yield plot
                    return  # /* last pixel -> curve finished */
                y1 = 2 * err < dx  # /* save value for test of y step */
                if 2 * err > dy:
                    x0 += sx
                    dx -= xy
                    dy += yy
                    err += dy
                    # /* x step */
                if y1 != 0:
                    y0 += sy
                    dy -= xy
                    dx += xx
                    err += dx
                    # /* y step */
                if not (dy < 0 < dx):  # /* gradient negates -> algorithm fails */
                    break
        for plot in Line.plot_line(x0, y0, x2, y2):  # /* plot remaining part to end */:
            if points is None:
                yield plot  # /* plot curve */
            else:
                points.append(plot)  # plotLine(x0,y0, x2,y2) #/* plot remaining part to end */
        if points is not None:
            for plot in reversed(points):
                yield plot

    @staticmethod
    def plot_quad_bezier(x0, y0, x1, y1, x2, y2):
        """Zingl-Bresenham quad bezier draw algorithm.
        plot any quadratic Bezier curve"""
        x0 = int(x0)
        y0 = int(y0)
        # control points are permitted fractional elements.
        x2 = int(x2)
        y2 = int(y2)
        x = x0 - x1
        y = y0 - y1
        t = x0 - 2 * x1 + x2
        r = 0

        if x * (x2 - x1) > 0:  # /* horizontal cut at P4? */
            if y * (y2 - y1) > 0:  # /* vertical cut at P6 too? */
                if abs((y0 - 2 * y1 + y2) / t * x) > abs(y):  # /* which first? */
                    x0 = x2
                    x2 = x + x1
                    y0 = y2
                    y2 = y + y1  # /* swap points */
                    # /* now horizontal cut at P4 comes first */
            t = (x0 - x1) / t
            r = (1 - t) * ((1 - t) * y0 + 2.0 * t * y1) + t * t * y2  # /* By(t=P4) */
            t = (x0 * x2 - x1 * x1) * t / (x0 - x1)  # /* gradient dP4/dx=0 */
            x = floor(t + 0.5)
            y = floor(r + 0.5)
            r = (y1 - y0) * (t - x0) / (x1 - x0) + y0  # /* intersect P3 | P0 P1 */
            for plot in QuadraticBezier.plot_quad_bezier_seg(x0, y0, x, floor(r + 0.5), x, y):
                yield plot
            r = (y1 - y2) * (t - x2) / (x1 - x2) + y2  # /* intersect P4 | P1 P2 */
            x0 = x1 = x
            y0 = y
            y1 = floor(r + 0.5)  # /* P0 = P4, P1 = P8 */
        if (y0 - y1) * (y2 - y1) > 0:  # /* vertical cut at P6? */
            t = y0 - 2 * y1 + y2
            t = (y0 - y1) / t
            r = (1 - t) * ((1 - t) * x0 + 2.0 * t * x1) + t * t * x2  # /* Bx(t=P6) */
            t = (y0 * y2 - y1 * y1) * t / (y0 - y1)  # /* gradient dP6/dy=0 */
            x = floor(r + 0.5)
            y = floor(t + 0.5)
            r = (x1 - x0) * (t - y0) / (y1 - y0) + x0  # /* intersect P6 | P0 P1 */
            for plot in QuadraticBezier.plot_quad_bezier_seg(x0, y0, floor(r + 0.5), y, x, y):
                yield plot
            r = (x1 - x2) * (t - y2) / (y1 - y2) + x2  # /* intersect P7 | P1 P2 */
            x0 = x
            x1 = floor(r + 0.5)
            y0 = y1 = y  # /* P0 = P6, P1 = P7 */
        for plot in QuadraticBezier.plot_quad_bezier_seg(x0, y0, x1, y1, x2, y2):  # /* remaining part */
            yield plot


class CubicBezier(PathSegment):
    def __init__(self, start, control1, control2, end):
        PathSegment.__init__(self)
        self.end = None
        self.control1 = None
        self.control2 = None
        self.start = None
        if start is not None:
            self.start = Point(start)
        if control1 is not None:
            self.control1 = Point(control1)
        if control2 is not None:
            self.control2 = Point(control2)
        if end is not None:
            self.end = Point(end)

    def __repr__(self):
        return 'CubicBezier(start=%s, control1=%s, control2=%s, end=%s)' % (
            repr(self.start), repr(self.control1), repr(self.control2), repr(self.end))

    def __copy__(self):
        return CubicBezier(self.start, self.control1, self.control2, self.end)

    def __eq__(self, other):
        if not isinstance(other, CubicBezier):
            return NotImplemented
        return self.start == other.start and self.end == other.end and \
               self.control1 == other.control1 and self.control2 == other.control2

    def __ne__(self, other):
        if not isinstance(other, CubicBezier):
            return NotImplemented
        return not self == other

    def __imul__(self, other):
        if isinstance(other, Matrix):
            if self.start is not None:
                self.start *= other
            if self.control1 is not None:
                self.control1 *= other
            if self.control2 is not None:
                self.control2 *= other
            if self.end is not None:
                self.end *= other
        return self

    def __len__(self):
        return 4

    def __getitem__(self, item):
        if item == 0:
            return self.start
        elif item == 1:
            return self.control1
        elif item == 2:
            return self.control2
        elif item == 3:
            return self.end
        else:
            raise IndexError

    def reverse(self):
        PathSegment.reverse(self)
        c2 = self.control2
        self.control2 = self.control1
        self.control1 = c2

    def point(self, t):
        """Calculate the x,y position at a certain position of the path"""
        x0, y0 = self.start
        x1, y1 = self.control1
        x2, y2 = self.control2
        x3, y3 = self.end
        x = (1 - t) * (1 - t) * (1 - t) * x0 + 3 * (1 - t) * (1 - t) * t * x1 + 3 * (
                1 - t) * t * t * x2 + t * t * t * x3
        y = (1 - t) * (1 - t) * (1 - t) * y0 + 3 * (1 - t) * (1 - t) * t * y1 + 3 * (
                1 - t) * t * t * y2 + t * t * t * y3
        return Point(x, y)

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        """Calculate the length of the path up to a certain position"""
        start_point = self.point(0)
        end_point = self.point(1)
        return segment_length(self, 0, 1, start_point, end_point, error, min_depth, 0)

    def is_smooth_from(self, previous):
        """Checks if this segment would be a smooth segment following the previous"""
        if isinstance(previous, CubicBezier):
            return (self.start == previous.end and
                    (self.control1 - self.start) == (previous.end - previous.control2))
        else:
            return self.control1 == self.start

    def d(self, current_point=None, smooth=False):
        if smooth:
            if current_point is None:
                return 'S %s %s' % (self.control2, self.end)
            else:
                return 's %s %s' % (self.control2 - current_point, self.end - current_point)
        else:
            if current_point is None:
                return 'C %s %s %s' % (self.control1, self.control2, self.end)
            else:
                return 'c %s %s %s' % (
                    self.control1 - current_point, self.control2 - current_point, self.end - current_point)

    def plot(self):
        for e in CubicBezier.plot_cubic_bezier(self.start[0], self.start[1],
                                               self.control1[0], self.control1[1],
                                               self.control2[0], self.control2[1],
                                               self.end[0], self.end[1]):
            yield e

    @staticmethod
    def plot_cubic_bezier_seg(x0, y0, x1, y1, x2, y2, x3, y3):
        """plot limited cubic Bezier segment
        This algorithm can plot curves that do not inflect.
        It is used as part of the general algorithm, which breaks at the infection points"""
        second_leg = []
        f = 0
        fx = 0
        fy = 0
        leg = 1
        if x0 < x3:
            sx = 1
        else:
            sx = -1
        if y0 < y3:
            sy = 1  # /* step direction */
        else:
            sy = -1  # /* step direction */
        xc = -abs(x0 + x1 - x2 - x3)
        xa = xc - 4 * sx * (x1 - x2)
        xb = sx * (x0 - x1 - x2 + x3)
        yc = -abs(y0 + y1 - y2 - y3)
        ya = yc - 4 * sy * (y1 - y2)
        yb = sy * (y0 - y1 - y2 + y3)
        ab = 0
        ac = 0
        bc = 0
        cb = 0
        xx = 0
        xy = 0
        yy = 0
        dx = 0
        dy = 0
        ex = 0
        pxy = 0
        EP = 0.01
        # /* check for curve restrains */
        # /* slope P0-P1 == P2-P3 and  (P0-P3 == P1-P2    or  no slope change)
        # if (x1 - x0) * (x2 - x3) < EP and ((x3 - x0) * (x1 - x2) < EP or xb * xb < xa * xc + EP):
        #     return
        # if (y1 - y0) * (y2 - y3) < EP and ((y3 - y0) * (y1 - y2) < EP or yb * yb < ya * yc + EP):
        #     return

        if xa == 0 and ya == 0:  # /* quadratic Bezier */
            # return plot_quad_bezier_seg(x0, y0, (3 * x1 - x0) >> 1, (3 * y1 - y0) >> 1, x3, y3)
            sx = floor((3 * x1 - x0 + 1) / 2)
            sy = floor((3 * y1 - y0 + 1) / 2)  # /* new midpoint */

            for plot in QuadraticBezier.plot_quad_bezier_seg(x0, y0, sx, sy, x3, y3):
                yield plot
            return
        x1 = (x1 - x0) * (x1 - x0) + (y1 - y0) * (y1 - y0) + 1  # /* line lengths */
        x2 = (x2 - x3) * (x2 - x3) + (y2 - y3) * (y2 - y3) + 1

        while True:  # /* loop over both ends */
            ab = xa * yb - xb * ya
            ac = xa * yc - xc * ya
            bc = xb * yc - xc * yb
            ex = ab * (ab + ac - 3 * bc) + ac * ac  # /* P0 part of self-intersection loop? */
            if ex > 0:
                f = 1  # /* calc resolution */
            else:
                f = floor(sqrt(1 + 1024 / x1))  # /* calc resolution */
            ab *= f
            ac *= f
            bc *= f
            ex *= f * f  # /* increase resolution */
            xy = 9 * (ab + ac + bc) / 8
            cb = 8 * (xa - ya)  # /* init differences of 1st degree */
            dx = 27 * (8 * ab * (yb * yb - ya * yc) + ex * (ya + 2 * yb + yc)) / 64 - ya * ya * (xy - ya)
            dy = 27 * (8 * ab * (xb * xb - xa * xc) - ex * (xa + 2 * xb + xc)) / 64 - xa * xa * (xy + xa)
            # /* init differences of 2nd degree */
            xx = 3 * (3 * ab * (3 * yb * yb - ya * ya - 2 * ya * yc) - ya * (3 * ac * (ya + yb) + ya * cb)) / 4
            yy = 3 * (3 * ab * (3 * xb * xb - xa * xa - 2 * xa * xc) - xa * (3 * ac * (xa + xb) + xa * cb)) / 4
            xy = xa * ya * (6 * ab + 6 * ac - 3 * bc + cb)
            ac = ya * ya
            cb = xa * xa
            xy = 3 * (xy + 9 * f * (cb * yb * yc - xb * xc * ac) - 18 * xb * yb * ab) / 8

            if ex < 0:  # /* negate values if inside self-intersection loop */
                dx = -dx
                dy = -dy
                xx = -xx
                yy = -yy
                xy = -xy
                ac = -ac
                cb = -cb  # /* init differences of 3rd degree */
            ab = 6 * ya * ac
            ac = -6 * xa * ac
            bc = 6 * ya * cb
            cb = -6 * xa * cb
            dx += xy
            ex = dx + dy
            dy += xy  # /* error of 1st step */
            try:
                pxy = 0
                fx = fy = f
                while x0 != x3 and y0 != y3:
                    if leg == 0:
                        second_leg.append((x0, y0))  # /* plot curve */
                    else:
                        yield x0, y0  # /* plot curve */
                    while True:  # /* move sub-steps of one pixel */
                        if pxy == 0:
                            if dx > xy or dy < xy:
                                raise StopIteration  # /* confusing */
                        if pxy == 1:
                            if dx > 0 or dy < 0:
                                raise StopIteration  # /* values */
                        y1 = 2 * ex - dy  # /* save value for test of y step */
                        if 2 * ex >= dx:  # /* x sub-step */
                            fx -= 1
                            dx += xx
                            ex += dx
                            xy += ac
                            dy += xy
                            yy += bc
                            xx += ab
                        elif y1 > 0:
                            raise StopIteration
                        if y1 <= 0:  # /* y sub-step */
                            fy -= 1
                            dy += yy
                            ex += dy
                            xy += bc
                            dx += xy
                            xx += ac
                            yy += cb
                        if not (fx > 0 and fy > 0):  # /* pixel complete? */
                            break
                    if 2 * fx <= f:
                        x0 += sx
                        fx += f  # /* x step */
                    if 2 * fy <= f:
                        y0 += sy
                        fy += f  # /* y step */
                    if pxy == 0 and dx < 0 and dy > 0:
                        pxy = 1  # /* pixel ahead valid */
            except StopIteration:
                pass
            xx = x0
            x0 = x3
            x3 = xx
            sx = -sx
            xb = -xb  # /* swap legs */
            yy = y0
            y0 = y3
            y3 = yy
            sy = -sy
            yb = -yb
            x1 = x2
            if not (leg != 0):
                break
            leg -= 1  # /* try other end */
        for plot in Line.plot_line(x3, y3, x0, y0):  # /* remaining part in case of cusp or crunode */
            second_leg.append(plot)
        for plot in reversed(second_leg):
            yield plot

    @staticmethod
    def plot_cubic_bezier(x0, y0, x1, y1, x2, y2, x3, y3):
        """Zingl-Bresenham cubic bezier draw algorithm
        plot any quadratic Bezier curve"""
        x0 = int(x0)
        y0 = int(y0)
        # control points are permitted fractional elements.
        x3 = int(x3)
        y3 = int(y3)
        n = 0
        i = 0
        xc = x0 + x1 - x2 - x3
        xa = xc - 4 * (x1 - x2)
        xb = x0 - x1 - x2 + x3
        xd = xb + 4 * (x1 + x2)
        yc = y0 + y1 - y2 - y3
        ya = yc - 4 * (y1 - y2)
        yb = y0 - y1 - y2 + y3
        yd = yb + 4 * (y1 + y2)
        fx0 = x0
        fx1 = 0
        fx2 = 0
        fx3 = 0
        fy0 = y0
        fy1 = 0
        fy2 = 0
        fy3 = 0
        t1 = xb * xb - xa * xc
        t2 = 0
        t = [0] * 5
        # /* sub-divide curve at gradient sign changes */
        if xa == 0:  # /* horizontal */
            if abs(xc) < 2 * abs(xb):
                t[n] = xc / (2.0 * xb)  # /* one change */
                n += 1
        elif t1 > 0.0:  # /* two changes */
            t2 = sqrt(t1)
            t1 = (xb - t2) / xa
            if abs(t1) < 1.0:
                t[n] = t1
                n += 1
            t1 = (xb + t2) / xa
            if abs(t1) < 1.0:
                t[n] = t1
                n += 1
        t1 = yb * yb - ya * yc
        if ya == 0:  # /* vertical */
            if abs(yc) < 2 * abs(yb):
                t[n] = yc / (2.0 * yb)  # /* one change */
                n += 1
        elif t1 > 0.0:  # /* two changes */
            t2 = sqrt(t1)
            t1 = (yb - t2) / ya
            if abs(t1) < 1.0:
                t[n] = t1
                n += 1
            t1 = (yb + t2) / ya
            if abs(t1) < 1.0:
                t[n] = t1
                n += 1
        i = 1
        while i < n:  # /* bubble sort of 4 points */
            t1 = t[i - 1]
            if t1 > t[i]:
                t[i - 1] = t[i]
                t[i] = t1
                i = 0
            i += 1
        t1 = -1.0
        t[n] = 1.0  # /* begin / end point */
        for i in range(0, n + 1):  # /* plot each segment separately */
            t2 = t[i]  # /* sub-divide at t[i-1], t[i] */
            fx1 = (t1 * (t1 * xb - 2 * xc) - t2 * (t1 * (t1 * xa - 2 * xb) + xc) + xd) / 8 - fx0
            fy1 = (t1 * (t1 * yb - 2 * yc) - t2 * (t1 * (t1 * ya - 2 * yb) + yc) + yd) / 8 - fy0
            fx2 = (t2 * (t2 * xb - 2 * xc) - t1 * (t2 * (t2 * xa - 2 * xb) + xc) + xd) / 8 - fx0
            fy2 = (t2 * (t2 * yb - 2 * yc) - t1 * (t2 * (t2 * ya - 2 * yb) + yc) + yd) / 8 - fy0
            fx3 = (t2 * (t2 * (3 * xb - t2 * xa) - 3 * xc) + xd) / 8
            fx0 -= fx3
            fy3 = (t2 * (t2 * (3 * yb - t2 * ya) - 3 * yc) + yd) / 8
            fy0 -= fy3
            x3 = floor(fx3 + 0.5)
            y3 = floor(fy3 + 0.5)  # /* scale bounds */
            if fx0 != 0.0:
                fx0 = (x0 - x3) / fx0
                fx1 *= fx0
                fx2 *= fx0
            if fy0 != 0.0:
                fy0 = (y0 - y3) / fy0
                fy1 *= fy0
                fy2 *= fy0
            if x0 != x3 or y0 != y3:  # /* segment t1 - t2 */
                # plotCubicBezierSeg(x0,y0, x0+fx1,y0+fy1, x0+fx2,y0+fy2, x3,y3)
                for plot in CubicBezier.plot_cubic_bezier_seg(x0, y0, x0 + fx1, y0 + fy1, x0 + fx2, y0 + fy2, x3, y3):
                    yield plot
            x0 = x3
            y0 = y3
            fx0 = fx3
            fy0 = fy3
            t1 = t2


class Arc(PathSegment):
    def __init__(self, *args, **kwargs):
        """Arc objects can take different parameters to create arcs.
        Since we expect taking in SVG parameters. We accept SVG parameterization which is:
        start, rx, ry, rotation, arc_flag, sweep_flag, end.

        To do matrix transitions, the native parameterization is start, end, center, prx, pry, sweep

        'start, end, center, prx, pry' are points and sweep amount is a value in tau radians.
        If points are modified by an affine transformation, the arc is transformed.
        There is a special case for when the scale factor inverts, it inverts the sweep.

        prx is the point at angle 0 of the non-rotated ellipse.
        pry is the point at angle tau/4 of the non-rotated ellipse.
        The theta-rotation can be defined as the angle from center to prx

        The sweep angle can be a value greater than tau and less than -tau.
        However if this is the case conversion back to Path.d() is expected to fail.

        prx -> center -> pry should form a right triangle.
        angle(center,end) - angle(center, start) should equal sweep or mod thereof.

        start and end should fall on the ellipse defined by prx, pry and center.
        """
        PathSegment.__init__(self)
        self.start = None
        self.end = None
        self.center = None
        self.prx = None
        self.pry = None
        self.sweep = None
        if len(args) == 6 and isinstance(args[1], complex):
            self._svg_complex_parameterize(*args)
            return
        elif len(kwargs) == 6 and 'rotation' in kwargs:
            self._svg_complex_parameterize(**kwargs)
            return
        elif len(args) == 7:
            # This is an svg parameterized call.
            # A: rx ry x-axis-rotation large-arc-flag sweep-flag x y
            self._svg_parameterize(args[0], args[1], args[2], args[3], args[4], args[5], args[6])
            return
        # TODO: account for L, T, R, B, startAngle, endAngle, theta parameters.
        # cx = (left + right) / 2
        # cy = (top + bottom) / 2
        #
        # rx = (right - left) / 2
        # cy = (bottom - top) / 2
        # startAngle, endAngle, theta
        len_args = len(args)
        if len_args > 0:
            if args[0] is not None:
                self.start = Point(args[0])
        if len_args > 1:
            if args[1] is not None:
                self.end = Point(args[1])
        if len_args > 2:
            if args[2] is not None:
                self.center = Point(args[2])
        if len_args > 3:
            if args[3] is not None:
                self.prx = Point(args[3])
        if len_args > 4:
            if args[4] is not None:
                self.pry = Point(args[4])
        if len_args > 5:
            self.sweep = args[5]
            return  # The args gave us everything.
        if 'start' in kwargs:
            self.start = kwargs['start']
        if 'end' in kwargs:
            self.end = kwargs['end']
        if 'center' in kwargs:
            self.center = kwargs['center']
        if 'prx' in kwargs:
            self.prx = kwargs['prx']
        if 'pry' in kwargs:
            self.pry = kwargs['pry']
        if 'sweep' in kwargs:
            self.sweep = kwargs['sweep']
        if self.center is not None:
            if 'r' in kwargs:
                r = kwargs['r']
                if self.prx is None:
                    self.prx = [self.center[0] + r, self.center[1]]
                if self.pry is None:
                    self.pry = [self.center[0], self.center[1] + r]
            if 'rx' in kwargs:
                rx = kwargs['rx']
                if self.prx is None:
                    if 'rotation' in kwargs:
                        theta = kwargs['rotation']
                        self.prx = Point.polar(self.center, theta, rx)
                    else:
                        self.prx = [self.center[0] + rx, self.center[1]]
            if 'ry' in kwargs:
                ry = kwargs['ry']
                if self.pry is None:
                    if 'rotation' in kwargs:
                        theta = kwargs['rotation']
                        theta += tau / 4.0
                        self.pry = Point.polar(self.center, theta, ry)
                    else:
                        self.pry = [self.center[0], self.center[1] + ry]
            if self.start is not None and (self.prx is None or self.pry is None):
                radius_s = Point.distance(self.center, self.start)
                self.prx = Point(self.center[0] + radius_s, self.center[1])
                self.pry = Point(self.center[0], self.center[1] + radius_s)
            if self.end is not None and (self.prx is None or self.pry is None):
                radius_e = Point.distance(self.center, self.end)
                self.prx = Point(self.center[0] + radius_e, self.center[1])
                self.pry = Point(self.center[0], self.center[1] + radius_e)
            if self.sweep is None and self.start is not None and self.end is not None:
                start_angle = Point.angle(self.center, self.start)
                end_angle = Point.angle(self.center, self.end)
                self.sweep = end_angle - start_angle
            if self.sweep is not None and self.start is not None and self.end is None:
                start_angle = Point.angle(self.center, self.start)
                end_angle = start_angle + self.sweep
                r = Point.distance(self.center, self.start)
                self.end = Point.polar(self.center, end_angle, r)
            if self.sweep is not None and self.start is None and self.end is not None:
                end_angle = Point.angle(self.center, self.end)
                start_angle = end_angle - self.sweep
                r = Point.distance(self.center, self.end)
                self.start = Point.polar(self.center, start_angle, r)
        else:  # center is None
            pass

    def __repr__(self):
        return 'Arc(%s, %s, %s, %s, %s, %s)' % (
            repr(self.start), repr(self.end), repr(self.center), repr(self.prx), repr(self.pry), self.sweep)

    def __copy__(self):
        return Arc(self.start, self.end, self.center, self.prx, self.pry, self.sweep)

    def __eq__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        return self.start == other.start and self.end == other.end and \
               self.prx == other.prx and self.pry == other.pry and \
               self.center == other.center and self.sweep == other.sweep

    def __ne__(self, other):
        if not isinstance(other, Arc):
            return NotImplemented
        return not self == other

    def __imul__(self, other):
        if isinstance(other, Matrix):
            if self.start is not None:
                self.start *= other
            if self.center is not None:
                self.center *= other
            if self.end is not None:
                self.end *= other
            if self.prx is not None:
                self.prx *= other
            if self.pry is not None:
                self.pry *= other
            if other.value_scale_x() < 0:
                self.sweep = -self.sweep
            if other.value_scale_y() < 0:
                self.sweep = -self.sweep
        return self

    def __len__(self):
        return 5

    def __getitem__(self, item):
        if item == 0:
            return self.start
        elif item == 1:
            return self.end
        elif item == 2:
            return self.center
        elif item == 3:
            return self.prx
        elif item == 4:
            return self.pry
        raise IndexError

    @property
    def theta(self):
        """legacy property"""
        return self.get_start_angle().as_positive_degrees

    @property
    def delta(self):
        """legacy property"""
        return Angle.radians(self.sweep).as_degrees

    def point_at_angle(self, t):
        rotation = self.get_rotation()
        cos_theta_rotation = cos(rotation)
        sin_theta_rotation = sin(rotation)
        cos_angle = cos(t)
        sin_angle = sin(t)
        rx = self.rx
        ry = self.ry
        x = (cos_theta_rotation * cos_angle * rx - sin_theta_rotation * sin_angle * ry + self.center[0])
        y = (sin_theta_rotation * cos_angle * rx + cos_theta_rotation * sin_angle * ry + self.center[1])
        return Point(x, y)

    def reverse(self):
        PathSegment.reverse(self)
        self.sweep = -self.sweep

    def point(self, t):
        if self.start == self.end and self.sweep == 0:
            # This is equivalent of omitting the segment
            return self.start
        angle = self.get_start_angle() - self.get_rotation() + self.sweep * t
        return self.point_at_angle(angle)

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        """The length of an elliptical arc segment requires numerical
        integration, and in that case it's simpler to just do a geometric
        approximation, as for cubic bezier curves.
        """
        if self.sweep == 0:
            return 0
        if self.start == self.end and self.sweep == 0:
            # This is equivalent of omitting the segment
            return 0
        if self.rx == self.ry:  # This is a circle.
            return abs(self.rx * self.sweep)

        start_point = self.point(0)
        end_point = self.point(1)
        return segment_length(self, 0, 1, start_point, end_point, error, min_depth, 0)

    def _svg_complex_parameterize(self, start, radius, rotation, arc, sweep, end):
        """Parameterization with complex radius and having rotation factors."""
        self._svg_parameterize(Point(start), radius.real, radius.imag, rotation, bool(arc), bool(sweep), Point(end))

    def _svg_parameterize(self, start, rx, ry, rotation, large_arc_flag, sweep_flag, end):
        """Conversion from svg parameterization, our chosen native native form.
        http://www.w3.org/TR/SVG/implnote.html#ArcImplementationNotes """

        start = Point(start)
        self.start = start
        end = Point(end)
        self.end = end
        if start == end:
            # If start is equal to end, there are infinite number of circles so these void out.
            # We still permit this kind of arc, but SVG parameterization cannot be used to achieve it.
            self.sweep = 0
            self.prx = Point(start)
            self.pry = Point(start)
            self.center = Point(start)
            return
        cosr = cos(radians(rotation))
        sinr = sin(radians(rotation))
        dx = (start.real - end.real) / 2
        dy = (start.imag - end.imag) / 2
        x1prim = cosr * dx + sinr * dy
        x1prim_sq = x1prim * x1prim
        y1prim = -sinr * dx + cosr * dy
        y1prim_sq = y1prim * y1prim

        rx_sq = rx * rx
        ry_sq = ry * ry

        # Correct out of range radii
        radius_check = (x1prim_sq / rx_sq) + (y1prim_sq / ry_sq)
        if radius_check > 1:
            rx *= sqrt(radius_check)
            ry *= sqrt(radius_check)
            rx_sq = rx * rx
            ry_sq = ry * ry

        t1 = rx_sq * y1prim_sq
        t2 = ry_sq * x1prim_sq
        c = sqrt(abs((rx_sq * ry_sq - t1 - t2) / (t1 + t2)))

        if large_arc_flag == sweep_flag:
            c = -c
        cxprim = c * rx * y1prim / ry
        cyprim = -c * ry * x1prim / rx

        center = Point((cosr * cxprim - sinr * cyprim) +
                       ((start.real + end.real) / 2),
                       (sinr * cxprim + cosr * cyprim) +
                       ((start.imag + end.imag) / 2))

        ux = (x1prim - cxprim) / rx
        uy = (y1prim - cyprim) / ry
        vx = (-x1prim - cxprim) / rx
        vy = (-y1prim - cyprim) / ry
        n = sqrt(ux * ux + uy * uy)
        p = ux
        theta = degrees(acos(p / n))
        if uy < 0:
            theta = -theta
        theta = theta % 360

        n = sqrt((ux * ux + uy * uy) * (vx * vx + vy * vy))
        p = ux * vx + uy * vy
        d = p / n
        # In certain cases the above calculation can through inaccuracies
        # become just slightly out of range, f ex -1.0000000000000002.
        if d > 1.0:
            d = 1.0
        elif d < -1.0:
            d = -1.0
        delta = degrees(acos(d))
        if (ux * vy - uy * vx) < 0:
            delta = -delta
        delta = delta % 360
        if not sweep_flag:
            delta -= 360
        # built parameters, delta, theta, center

        rotate_matrix = Matrix()
        rotate_matrix.post_rotate(Angle.degrees(rotation).as_radians, center[0], center[1])

        self.center = center
        self.prx = Point(center[0] + rx, center[1])
        self.pry = Point(center[0], center[1] + ry)

        self.prx.matrix_transform(rotate_matrix)
        self.pry.matrix_transform(rotate_matrix)
        self.sweep = Angle.degrees(delta).as_radians

    def as_quad_curves(self):
        sweep_limit = tau / 12
        arc_required = int(ceil(abs(self.sweep) / sweep_limit))
        if arc_required == 0:
            return
        slice = self.sweep / float(arc_required)

        start_angle = self.get_start_angle()
        theta = self.get_rotation()
        p_start = self.start
        p_end = self.end

        current_angle = start_angle - theta

        for i in range(0, arc_required):
            next_angle = current_angle + slice
            q = Point(p_start[0] + tan((p_end[0] - p_start[0]) / 2.0))
            yield QuadraticBezier(p_start, q, p_end)
            p_start = Point(p_end)
            current_angle = next_angle

    def as_cubic_curves(self):
        sweep_limit = tau / 12
        arc_required = int(ceil(abs(self.sweep) / sweep_limit))
        if arc_required == 0:
            return
        slice = self.sweep / float(arc_required)

        start_angle = self.get_start_angle()
        theta = self.get_rotation()
        rx = self.rx
        ry = self.ry
        p_start = self.start
        current_angle = start_angle - theta
        x0 = self.center[0]
        y0 = self.center[1]
        cos_theta = cos(theta)
        sin_theta = sin(theta)

        for i in range(0, arc_required):
            next_angle = current_angle + slice

            alpha = sin(slice) * (sqrt(4 + 3 * pow(tan((slice) / 2.0), 2)) - 1) / 3.0

            cos_start_angle = cos(current_angle)
            sin_start_angle = sin(current_angle)

            ePrimen1x = -rx * cos_theta * sin_start_angle - ry * sin_theta * cos_start_angle
            ePrimen1y = -rx * sin_theta * sin_start_angle + ry * cos_theta * cos_start_angle

            cos_end_angle = cos(next_angle)
            sin_end_angle = sin(next_angle)

            p2En2x = x0 + rx * cos_end_angle * cos_theta - ry * sin_end_angle * sin_theta
            p2En2y = y0 + rx * cos_end_angle * sin_theta + ry * sin_end_angle * cos_theta
            p_end = (p2En2x, p2En2y)
            if i == arc_required - 1:
                p_end = self.end

            ePrimen2x = -rx * cos_theta * sin_end_angle - ry * sin_theta * cos_end_angle
            ePrimen2y = -rx * sin_theta * sin_end_angle + ry * cos_theta * cos_end_angle

            p_c1 = (p_start[0] + alpha * ePrimen1x, p_start[1] + alpha * ePrimen1y)
            p_c2 = (p_end[0] - alpha * ePrimen2x, p_end[1] - alpha * ePrimen2y)

            yield CubicBezier(p_start, p_c1, p_c2, p_end)
            p_start = Point(p_end)
            current_angle = next_angle

    def is_circular(self):
        a = self.rx
        b = self.ry
        return a == b

    @property
    def radius(self):
        """Legacy complex radius property

        Point will work like a complex for legacy reasons.
        """
        return Point(self.rx, self.ry)

    @property
    def rx(self):
        return Point.distance(self.center, self.prx)

    @property
    def ry(self):
        return Point.distance(self.center, self.pry)

    def get_rotation(self):
        return Point.angle(self.center, self.prx)

    def get_start_angle(self):
        return Point.angle(self.center, self.start)

    def get_end_angle(self):
        return Point.angle(self.center, self.end)

    def bbox(self):
        """Returns the bounding box of the arc."""
        # TODO: truncated the bounding box to the arc rather than the entire ellipse.
        theta = Point.angle(self.center, self.prx)
        a = Point.distance(self.center, self.prx)
        b = Point.distance(self.center, self.pry)
        cos_theta = cos(theta)
        sin_theta = sin(theta)
        xmax = sqrt(a * a * cos_theta * cos_theta + b * b * sin_theta * sin_theta)
        xmin = -xmax
        ymax = sqrt(a * a * sin_theta * sin_theta + b * b * cos_theta * cos_theta)
        ymin = -xmax
        return xmin + self.center[0], ymin + self.center[1], xmax + self.center[0], ymax + self.center[1]

    def d(self, current_point=None, smooth=False):
        if current_point is None:
            return 'A %G,%G %G %d,%d %s' % (
                self.rx,
                self.ry,
                self.get_rotation().as_degrees,
                int(abs(self.sweep) > (tau / 2.0)),
                int(self.sweep >= 0),
                self.end)
        else:
            return 'a %G,%G %G %d,%d %s' % (
                self.rx,
                self.ry,
                self.get_rotation().as_degrees,
                int(abs(self.sweep) > (tau / 2.0)),
                int(self.sweep >= 0),
                self.end - current_point)

    def plot(self):
        # TODO: Should actually plot the arc according to the pixel-perfect standard. In this case we would plot a
        # Bernstein weighted bezier curve.
        for curve in self.as_cubic_curves():
            for value in curve.plot():
                yield value


class Path(MutableSequence):
    """A Path is a sequence of path segments"""

    def __init__(self, *segments):
        self._length = None
        self._lengths = None
        if len(segments) == 1:
            if isinstance(segments[0], Subpath):
                self._segments = []
                self._segments.extend(map(copy, list(segments[0])))
                return
            elif isinstance(segments[0], str):
                self._segments = list()
                self.parse(segments[0])
                return
            elif isinstance(segments[0], list):
                self._segments = segments[0]
                return
        self._segments = list(segments)

    def __copy__(self):
        return Path(*map(copy, self._segments))

    def __getitem__(self, index):
        return self._segments[index]

    def __setitem__(self, index, value):
        self._segments[index] = value
        self._length = None

    def __delitem__(self, index):
        del self._segments[index]
        self._length = None

    def __iadd__(self, other):
        if isinstance(other, str):
            self.parse(other)
        elif isinstance(other, (Path, Subpath)):
            self._segments.extend(map(copy, list(other)))
        elif isinstance(other, PathSegment):
            self.append(other)
        else:
            return NotImplemented
        self.validate_connections()
        return self

    def __add__(self, other):
        n = copy(self)
        n += other
        return n

    def __radd__(self, other):
        if isinstance(other, str):
            path = Path(other)
            path.extend(map(copy, self._segments))
            path.validate_connections()
            return path
        elif isinstance(other, PathSegment):
            path = copy(self)
            path.insert(0, other)
            path.validate_connections()
            return path
        else:
            return NotImplemented

    def __imul__(self, other):
        if isinstance(other, str):
            other = Matrix(other)
        if isinstance(other, Matrix):
            for e in self._segments:
                e *= other
        return self

    def __mul__(self, other):
        if isinstance(other, (Matrix, str)):
            n = copy(self)
            n *= other
            return n

    __rmul__ = __mul__

    def __len__(self):
        return len(self._segments)

    def __str__(self):
        return self.d()

    def __repr__(self):
        return 'Path(%s)' % (', '.join(repr(x) for x in self._segments))

    def __eq__(self, other):
        if isinstance(other, str):
            return self.__eq__(Path(other))
        if not isinstance(other, Path):
            return NotImplemented
        if len(self) != len(other):
            return False
        for s, o in zip(self._segments, other._segments):
            if not s == o:
                return False
        return True

    def __ne__(self, other):
        if not isinstance(other, (Path, str)):
            return NotImplemented
        return not self == other

    def parse(self, pathdef):
        """Parses the SVG path."""
        tokens = SVGPathTokens()
        tokens.svg_parse(self, pathdef)

    def validate_connections(self):
        """
        Validate path connections. This will scan path connections and link any adjacent elements together by replacing
        any None points or causing the start position of the next element to equal the end position of the previous.
        This should only be needed when combining paths and elements together. Close elements are always connected to
        the last Move element or to the end position of the first element in the list. The start element of the first
        segment may or may not be None. But, will not be regarded as important.

        This does not guarantee that the SVG path is valid. It may still have no initial Move element, multiple Close
        elements, Arcs that cannot be denoted by SVG or segments that do not exist in SVG.

        There is no need to call this directly as it will be invoked on any changes to Path.
        """
        zpoint = None
        last_segment = None
        for segment in self._segments:
            if zpoint is None or isinstance(segment, Move):
                zpoint = segment.end
            if last_segment is not None:
                if segment.start is None and last_segment.end is not None:
                    segment.start = Point(last_segment.end)
                elif last_segment.end is None and segment.start is not None:
                    last_segment.end = Point(segment.start)
                elif last_segment.end != segment.start:
                    segment.start = Point(last_segment.end)
            if isinstance(segment, Close) and zpoint is not None and segment.end != zpoint:
                segment.end = Point(zpoint)
            last_segment = segment

    @property
    def first_point(self):
        """First point along the Path. This is the start point of the first segment unless it starts
        with a Move command with a None start in which case first point is that Move's destination."""
        if len(self._segments) == 0:
            return None
        if self._segments[0].start is not None:
            return Point(self._segments[0].start)
        return Point(self._segments[0].end)

    @property
    def current_point(self):
        if len(self._segments) == 0:
            return None
        return Point(self._segments[-1].end)

    @property
    def z_point(self):
        """
        Z doesn't necessarily mean the first_point, it's the destination of the last Move.
        This behavior of Z is defined in svg spec:
        http://www.w3.org/TR/SVG/paths.html#PathDataClosePathCommand
        """
        end_pos = None
        for segment in reversed(self._segments):
            if isinstance(segment, Move):
                end_pos = segment.end
                break
        if end_pos is None:
            try:
                end_pos = self._segments[0].end
            except IndexError:
                pass  # entire path is "z".
        return end_pos

    @property
    def smooth_point(self):
        """Returns the smoothing control point for the smooth commands.
        With regards to the SVG standard if the last command was a curve the smooth
        control point is the reflection of the previous control point.

        If the last command was not a curve, the smooth_point is coincident with the current.
        https://www.w3.org/TR/SVG/paths.html#PathDataCubicBezierCommands
        """

        if len(self._segments) == 0:
            return None
        start_pos = self.current_point
        last_segment = self._segments[-1]
        if isinstance(last_segment, QuadraticBezier):
            previous_control = last_segment.control
            return previous_control.reflected_across(start_pos)
        elif isinstance(last_segment, CubicBezier):
            previous_control = last_segment.control2
            return previous_control.reflected_across(start_pos)
        return start_pos

    def start(self):
        pass

    def end(self):
        pass

    def move(self, *points):
        end_pos = points[0]
        # if len(self._segments) > 0:
        #     if isinstance(self._segments[-1], Move):
        #         # If there was just a move command update that.
        #         self._segments[-1].end = Point(end_pos)
        #         return
        start_pos = self.current_point
        self.append(Move(start_pos, end_pos))
        if len(points) > 1:
            self.line(*points[1:])

    def line(self, *points):
        start_pos = self.current_point
        end_pos = points[0]
        if end_pos == 'z':
            self.append(Line(start_pos, self.z_point))
            self.closed()
            return
        self.append(Line(start_pos, end_pos))
        if len(points) > 1:
            self.line(*points[1:])

    def absolute_v(self, *y_points):
        y_pos = y_points[0]
        start_pos = self.current_point
        self.append(Line(start_pos, Point(start_pos[0], y_pos)))
        if len(y_points) > 1:
            self.absolute_v(*y_points[1:])

    def relative_v(self, *dys):
        dy = dys[0]
        start_pos = self.current_point
        self.append(Line(start_pos, Point(start_pos[0], start_pos[1] + dy)))
        if len(dys) > 1:
            self.relative_v(*dys[1:])

    def absolute_h(self, *x_points):
        x_pos = x_points[0]
        start_pos = self.current_point
        self.append(Line(start_pos, Point(x_pos, start_pos[1])))
        if len(x_points) > 1:
            self.absolute_h(*x_points[1:])

    def relative_h(self, *dxs):
        dx = dxs[0]
        start_pos = self.current_point
        self.append(Line(start_pos, Point(start_pos[0] + dx, start_pos[1])))
        if len(dxs) > 1:
            self.relative_h(*dxs[1:])

    def smooth_quad(self, *points):
        """Smooth curve. First control point is the "reflection" of
           the second control point in the previous path."""
        start_pos = self.current_point
        control1 = self.smooth_point
        end_pos = points[0]
        if end_pos == 'z':
            self.append(QuadraticBezier(start_pos, control1, self.z_point))
            self.closed()
            return
        self.append(QuadraticBezier(start_pos, control1, end_pos))
        if len(points) > 1:
            self.smooth_quad(*points[1:])

    def quad(self, *points):
        start_pos = self.current_point
        control = points[0]
        if control == 'z':
            self.append(QuadraticBezier(start_pos, self.z_point, self.z_point))
            self.closed()
            return
        end_pos = points[1]
        if end_pos == 'z':
            self.append(QuadraticBezier(start_pos, control, self.z_point))
            self.closed()
            return
        self.append(QuadraticBezier(start_pos, control, end_pos))
        if len(points) > 2:
            self.quad(*points[2:])

    def smooth_cubic(self, *points):
        """Smooth curve. First control point is the "reflection" of
        the second control point in the previous path."""
        start_pos = self.current_point
        control1 = self.smooth_point
        control2 = points[0]
        if control2 == 'z':
            self.append(CubicBezier(start_pos, control1, self.z_point, self.z_point))
            self.closed()
            return
        end_pos = points[1]
        if end_pos == 'z':
            self.append(CubicBezier(start_pos, control1, control2, self.z_point))
            self.closed()
            return
        self.append(CubicBezier(start_pos, control1, control2, end_pos))
        if len(points) > 2:
            self.smooth_cubic(*points[2:])

    def cubic(self, *points):
        start_pos = self.current_point
        control1 = points[0]
        if control1 == 'z':
            self.append(CubicBezier(start_pos, self.z_point, self.z_point, self.z_point))
            self.closed()
            return
        control2 = points[1]
        if control2 == 'z':
            self.append(CubicBezier(start_pos, control1, self.z_point, self.z_point))
            self.closed()
            return
        end_pos = points[2]
        if end_pos == 'z':
            self.append(CubicBezier(start_pos, control1, control2, self.z_point))
            self.closed()
            return
        self.append(CubicBezier(start_pos, control1, control2, end_pos))
        if len(points) > 3:
            self.cubic(*points[3:])

    def arc(self, *arc_args):
        start_pos = self.current_point
        rx = arc_args[0]
        ry = arc_args[1]
        rotation = arc_args[2]
        arc = arc_args[3]
        sweep = arc_args[4]
        end_pos = arc_args[5]
        if end_pos == 'z':
            self.append(Arc(start_pos, rx, ry, rotation, arc, sweep, self.z_point))
            self.closed()
            return
        self.append(Arc(start_pos, rx, ry, rotation, arc, sweep, end_pos))
        if len(arc_args) > 6:
            self.arc(*arc_args[6:])

    def closed(self):
        start_pos = self.current_point
        end_pos = self.z_point
        self.append(Close(start_pos, end_pos))

    def _calc_lengths(self, error=ERROR, min_depth=MIN_DEPTH):
        if self._length is not None:
            return

        lengths = [each.length(error=error, min_depth=min_depth) for each in self._segments]
        self._length = sum(lengths)
        self._lengths = [each / self._length for each in lengths]

    def point(self, pos, error=ERROR):
        if len(self._segments) == 0:
            return None
        # Shortcuts
        if pos <= 0.0:
            return self._segments[0].point(pos)
        if pos >= 1.0:
            return self._segments[-1].point(pos)

        self._calc_lengths(error=error)
        # Find which segment the point we search for is located on:
        segment_start = 0
        segment_pos = 0
        segment = self._segments[0]
        for index, segment in enumerate(self._segments):
            segment_end = segment_start + self._lengths[index]
            if segment_end >= pos:
                # This is the segment! How far in on the segment is the point?
                segment_pos = (pos - segment_start) / (segment_end - segment_start)
                break
            segment_start = segment_end
        return segment.point(segment_pos)

    def length(self, error=ERROR, min_depth=MIN_DEPTH):
        self._calc_lengths(error, min_depth)
        return self._length

    def plot(self):
        for segment in self._segments:
            for e in segment.plot():
                yield e

    def insert(self, index, object):
        self._segments.insert(index, object)
        self._length = None
        self.validate_connections()

    def extend(self, iterable):
        self._segments.extend(iterable)
        self._length = None
        self.validate_connections()

    def reverse(self):
        if len(self._segments) == 0:
            return
        prepoint = self._segments[0].start
        self._segments[0].start = None
        p = Path()
        subpaths = list(self.as_subpaths())
        for subpath in subpaths:
            subpath.reverse()
        for subpath in reversed(subpaths):
            p += subpath
        self._segments = p._segments
        self._segments[0].start = prepoint
        return self

    def subpath(self, index):
        subpaths = list(self.as_subpaths())
        return subpaths[index]

    def count_subpaths(self):
        subpaths = list(self.as_subpaths())
        return len(subpaths)

    def as_subpaths(self):
        last = 0
        for current, seg in enumerate(self):
            if current != last and isinstance(seg, Move):
                yield Subpath(self, last, current - 1)
                last = current
        yield Subpath(self, last, len(self) - 1)

    def as_points(self):
        """Returns the list of defining points within path"""
        for seg in self:
            for p in seg:
                if not isinstance(p, Point):
                    yield Point(p)
                else:
                    yield p

    def bbox(self):
        """returns a bounding box for the input Path"""
        bbs = [seg.bbox() for seg in self._segments if not isinstance(Close, Move)]
        try:
            xmins, ymins, xmaxs, ymaxs = list(zip(*bbs))
        except ValueError:
            return None  # No bounding box items existed. So no bounding box.
        xmin = min(xmins)
        xmax = max(xmaxs)
        ymin = min(ymins)
        ymax = max(ymaxs)
        return xmin, ymin, xmax, ymax

    @staticmethod
    def svg_d(segments, relative=False):
        if len(segments) == 0:
            return ''
        if relative:
            return Path.svg_d_relative(segments)
        else:
            return Path.svg_d_absolute(segments)

    @staticmethod
    def svg_d_relative(segments):
        parts = []
        previous_segment = None
        p = Point(0)
        for segment in segments:
            if isinstance(segment, (Move, Line, Arc, Close)):
                parts.append(segment.d(p))
            elif isinstance(segment, (CubicBezier, QuadraticBezier)):
                parts.append(segment.d(p, smooth=segment.is_smooth_from(previous_segment)))
            previous_segment = segment
            p = previous_segment.end
        return ' '.join(parts)

    @staticmethod
    def svg_d_absolute(segments):
        parts = []
        previous_segment = None
        for segment in segments:
            if isinstance(segment, (Move, Line, Arc, Close)):
                parts.append(segment.d())
            elif isinstance(segment, (CubicBezier, QuadraticBezier)):
                parts.append(segment.d(smooth=segment.is_smooth_from(previous_segment)))
            previous_segment = segment
            p = previous_segment.end
        return ' '.join(parts)

    def d(self, relative=False):
        return Path.svg_d(self._segments, relative)


class Subpath:
    """Subpath is a Path-backed window implementation. It does not store a list of segments but rather
    stores a Path, start position, end position. When a function is called on a subpath, the result of those events
    occurs is performed on the backing Path. When the backing Path is modified the behavior is undefined."""

    def __init__(self, path, start, end):
        self._path = path
        self._start = start
        self._end = end

    def __copy__(self):
        p = Path()
        for seg in self._path:
            p.append(copy(seg))
        return p

    def __getitem__(self, index):
        if index < 0:
            index = self._end + index + 1
        else:
            index = self._start + index
        return self._path[index]

    def __setitem__(self, index, value):
        if index < 0:
            index = self._end + index + 1
        else:
            index = self._start + index
        self._path[index] = value

    def __delitem__(self, index):
        if index < 0:
            index = self._end + index + 1
        else:
            index = self._start + index
        del self._path[index]
        self._end -= 1

    def __iadd__(self, other):
        if isinstance(other, str):
            p = Path(other)
            self._path[self._end:self._end] = p
        elif isinstance(other, Path):
            p = copy(other)
            self._path[self._end:self._end] = p
        elif isinstance(other, PathSegment):
            self._path.insert(self._end, other)
        else:
            return NotImplemented
        return self

    def __add__(self, other):
        n = copy(self)
        n += other
        return n

    def __radd__(self, other):
        if isinstance(other, str):
            path = Path(other)
            path.extend(map(copy, self._path))
            return path
        elif isinstance(other, PathSegment):
            path = Path(self)
            path.insert(0, other)
            return path
        else:
            return NotImplemented

    def __imul__(self, other):
        if isinstance(other, str):
            other = Matrix(other)
        if isinstance(other, Matrix):
            for e in self:
                e *= other
        return self

    def __mul__(self, other):
        if isinstance(other, (Matrix, str)):
            n = copy(self)
            n *= other
            return n

    __rmul__ = __mul__

    def __iter__(self):
        class Iterator:
            def __init__(self, subpath):
                self.n = subpath._start - 1
                self.subpath = subpath

            def __next__(self):
                self.n += 1
                try:
                    if self.n > self.subpath._end:
                        raise StopIteration
                    return self.subpath._path[self.n]
                except IndexError:
                    raise StopIteration

            next = __next__

        return Iterator(self)

    def __len__(self):
        return self._end - self._start + 1

    def __str__(self):
        return self.d()

    def __repr__(self):
        return 'Path(%s)' % (', '.join(repr(x) for x in self))

    def __eq__(self, other):
        if isinstance(other, str):
            return self.__eq__(Path(other))
        if not isinstance(other, Path, Subpath):
            return NotImplemented
        if len(self) != len(other):
            return False
        for s, o in zip(self, other):
            if not s == o:
                return False
        return True

    def __ne__(self, other):
        if not isinstance(other, (Path, Subpath, str)):
            return NotImplemented
        return not self == other

    def bbox(self):
        """returns a bounding box for the input Path"""
        segments = self._path._segments[self._start:self._end + 1]
        bbs = [seg.bbox() for seg in segments if not isinstance(Close, Move)]
        try:
            xmins, ymins, xmaxs, ymaxs = list(zip(*bbs))
        except ValueError:
            return None  # No bounding box items existed. So no bounding box.
        xmin = min(xmins)
        xmax = max(xmaxs)
        ymin = min(ymins)
        ymax = max(ymaxs)
        return xmin, ymin, xmax, ymax

    def d(self, relative=False):
        segments = self._path._segments[self._start:self._end + 1]
        return Path.svg_d(segments, relative)

    def _reverse_segments(self, start, end):
        """Reverses segments within between the given indexes in the subpath space."""
        while start <= end:
            start_segment = self[start]
            end_segment = self[end]
            start_segment.reverse()
            if start_segment is not end_segment:
                end_segment.reverse()
                self[start] = end_segment
                self[end] = start_segment
            start += 1
            end -= 1

    def reverse(self):
        size = len(self)
        if size == 0:
            return
        start = 0
        end = size - 1
        if isinstance(self[-1], Close):
            end -= 1
        if isinstance(self[0], Move):  # Move remains in place but references next element.
            start += 1
        self._reverse_segments(start, end)
        if size > 1:
            if isinstance(self[0], Move):
                self[0].end = Point(self[1].start)
        last = self[-1]
        if isinstance(last, Close):
            last.reverse()
            if last.start != self[-2].end:
                last.start = Point(self[-2].end)
            if last.end != self[0].end:
                last.end = Point(self[0].end)
        return self


class SVG:
    """Main svg parsing of files. The file currently only supports nodes which are dictionary objects with
    svg attributes. These can then be converted into various elements through the various parsing methods."""

    def __init__(self, f):
        self.f = f

    # SVG File Parsing
    def nodes(self, viewport_transform=False):
        """Parses the SVG file.
        Style elements are split into their proper values.
        Transform elements are concatenated and unparsed.
        Leaf node elements are turned into pathd values."""

        f = self.f
        stack = []
        values = {}
        for event, elem in iterparse(f, events=('start', 'end')):
            if event == 'start':
                stack.append(values)
                current_values = values
                values = {}
                values.update(current_values)  # copy of dictionary

                attributes = elem.attrib
                if SVG_ATTR_STYLE in attributes:
                    for equate in attributes[SVG_ATTR_STYLE].split(";"):
                        equal_item = equate.split(":")
                        if len(equal_item) == 2:
                            attributes[equal_item[0]] = equal_item[1]
                if SVG_ATTR_TRANSFORM in attributes:
                    new_transform = attributes[SVG_ATTR_TRANSFORM]
                    if SVG_ATTR_TRANSFORM in values:
                        current_transform = values[SVG_ATTR_TRANSFORM]
                        attributes[SVG_ATTR_TRANSFORM] = current_transform + " " + new_transform
                    else:
                        attributes[SVG_ATTR_TRANSFORM] = new_transform
                    # will be used to update values.
                values.update(attributes)
                tag = elem.tag
                if tag.startswith('{'):
                    tag = tag[28:]  # Removing namespace. http://www.w3.org/2000/svg:
                if SVG_NAME_TAG == tag:
                    if viewport_transform:
                        new_transform = parse_viewbox_transform(values)
                        values[SVG_VIEWBOX_TRANSFORM] = new_transform
                        if SVG_ATTR_TRANSFORM in attributes:
                            values[SVG_ATTR_TRANSFORM] += " " + new_transform
                        else:
                            values[SVG_ATTR_TRANSFORM] = new_transform
                    yield values
                    continue
                elif SVG_TAG_GROUP == tag:
                    continue
                elif SVG_TAG_PATH == tag:
                    values[SVG_ATTR_DATA] = path2pathd(values)
                elif SVG_TAG_CIRCLE == tag:
                    values[SVG_ATTR_DATA] = ellipse2pathd(values)
                elif SVG_TAG_ELLIPSE == tag:
                    values[SVG_ATTR_DATA] = ellipse2pathd(values)
                elif SVG_TAG_LINE == tag:
                    values[SVG_ATTR_DATA] = line2pathd(values)
                elif SVG_TAG_POLYLINE == tag:
                    values[SVG_ATTR_DATA] = polyline2pathd(values)
                elif SVG_TAG_POLYGON == tag:
                    values[SVG_ATTR_DATA] = polygon2pathd(values)
                elif SVG_TAG_RECT == tag:
                    values[SVG_ATTR_DATA] = rect2pathd(values)
                elif SVG_TAG_IMAGE == tag:  # Has no pathd data, but yields as element.
                    if XLINK_HREF in values:
                        image = values[XLINK_HREF]
                    elif SVG_HREF in values:
                        image = values[SVG_HREF]
                    else:
                        continue
                    values[SVG_TAG_IMAGE] = image
                else:
                    continue
                values[SVG_ATTR_TAG] = tag
                yield values
            else:  # End event.
                # The iterparse spec makes it clear that internal text data is undefined except at the end.
                tag = elem.tag
                if tag.startswith('{'):
                    tag = tag[28:]  # Removing namespace. http://www.w3.org/2000/svg:
                if SVG_TAG_TEXT == tag:
                    values[SVG_ATTR_TAG] = tag
                    values[SVG_TAG_TEXT] = elem.text
                    yield values
                elif SVG_TAG_DESC == tag:
                    values[SVG_ATTR_TAG] = tag
                    values[SVG_TAG_DESC] = elem.text
                    yield values
                values = stack.pop()
