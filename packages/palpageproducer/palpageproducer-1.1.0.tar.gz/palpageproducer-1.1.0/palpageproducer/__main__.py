#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 garrick. Some rights reserved.
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Generate HTML palette pages from SASS/LESS/GPL palettes."""

import sys
import os
import math
from slugify import slugify_url
from appdirs import *

name = "palpageproducer"
author = "gargargarrick"
__author__ = "gargargarrick"
__version__ = '1.1.0'
__copyright__ = "Copyright 2019 Matthew Ellison"
__license__ = "GPL"
__maintainer__ = "gargargarrick"

def getFile():
    """Get the file to process."""
    if len(sys.argv) > 1:
        f = sys.argv[1]
    else:
        f = input("SASS/LESS/GPL file? > ")
    f_abspath = os.path.abspath(f)
    return(f_abspath)

def openSass(sasspath):
    """Read from a SASS .scss file."""
    with open(sasspath, "r") as fin:
        sass_s = fin.read().splitlines()
    return(sass_s)

def openLess(lesspath):
    """Read from a LESS .less file."""
    with open(lesspath, "r") as fin:
        less_s = fin.read().splitlines()
    less_replaced = []
    # P. much convert the important parts to SASS.
    for line in less_s:
        if line != "":
            line = line.strip()
            if line[0] == "@":
                newl = "${line}".format(line=line[1:])
                less_replaced.append(newl)
    return(less_replaced)

def rgbToHex(rgb):
    """Convert RGB colors into hex."""
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    h = "#{:02X}{:02X}{:02X}".format(r, g, b)
    return(h)

def openGimp(gpl_f):
    """Open a GIMP .gpl palette and process it."""
    with open(gpl_f, "r") as fin:
        gpl_raw = fin.read()
    gpl_s = gpl_raw.split("\n")[4:]
    new = []
    for x in gpl_s:
        if x is not None and x is not "":
            pair = x.strip().split("\t", 1)
            rgb = pair[0]
            name = pair[1]
            rgb = " ".join(rgb.split())
            rgb = tuple(rgb.split(" "))
            hex = rgbToHex(rgb)
            slugname = slugify_url(name, separator="_")
            finalu = "${name}: {hex}".format(
                name=slugname,
                hex=hex
            )
            new.append(finalu)
    return(new)

def findDivisor(count):
    """Find divisors below 5 (for determining column count)"""
    foo = reversed(range(1, 6))
    for i in foo:
        if count % i == 0:
            return(i)

def getColumns(count):
    """Set the number of columns for the output."""
    columns = findDivisor(count)
    if columns == 1:
        columns = 5
        vw = "20"
    else:
        vw = str(int(100 // columns))
    return(vw, str(columns))

def wrapInTag(content, tag):
    """Wrap something in an HTML tag"""
    return("<{tag}>{content}</{tag}>".format(
        tag=tag,
        content=content)
    )

def getLuminance(hex):
    """Get the luminance of a hex color"""
    hex_nohash = hex.lstrip("#")
    if len(hex_nohash) == 3:
        hex_nohash = "".join([item * 2 for item in hex_nohash])
    r, g, b = tuple(int(hex_nohash[i:i + 2], 16) for i in (0, 2, 4))
    rgbs = [r, g, b]
    rgbgs = []
    for component in rgbs:
        if component <= 10:
            adjusted = component / 3294
        else:
            adjusted = (component / 269 + 0.0513)**2.4
        rgbgs.append(adjusted)
    lum = 0.2126 * rgbgs[0] + 0.7152 * rgbgs[1] + 0.0722 * rgbgs[2]
    return(lum)

def checkContrast(hex):
    """Check the contrast between a hex color and black"""
    foreground = 0.0
    background = getLuminance(hex)
    colors = [foreground, background]
    ratio = (max(colors) + 0.05) / (min(colors) + 0.05)
    return(ratio)

def main():
    """Read a stylesheet/palette and generate an HTML page."""
    save_path = os.path.join(user_data_dir(name, author), "output")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    sass_f = getFile()
    sass_basename = os.path.basename(sass_f)
    sass_noext = os.path.splitext(sass_basename)[0]
    sass_noext_safe = slugify_url(sass_noext, separator="_")
    if os.path.splitext(sass_basename)[1] == ".scss":
        sass = openSass(sass_f)
    elif os.path.splitext(sass_basename)[1] == ".gpl":
        sass = openGimp(sass_f)
    elif os.path.splitext(sass_basename)[1] == ".less":
        sass = openLess(sass_f)

    title = wrapInTag(tag="title", content=sass_basename)
    h1 = wrapInTag(tag="h1", content=sass_basename)

    # Make sure the colors really are colors.
    really_colors = []
    for color in sass:
        color = color.strip()
        color = color.strip(";")
        if color != "" and color[0] == "$":
            colorid, colorvalue = color.split(": ", 1)
            if colorvalue[0] == "#":
                really_colors.append(color)
            # RGB colors are converted. RGBA colors are ignored.
            elif colorvalue[0:3] == "rgb" and colorvalue[0:4] != "rgba":
                norgb = colorvalue.strip("rgb()")
                justrgb = norgb.split(", ")
                hex = rgbToHex(justrgb)
                really_colors.append(
                    "{colorid}: {hex}".format(
                        colorid=colorid,
                        hex=hex)
                    )
            else:
                pass
    # Count the colors.
    colors = len(really_colors)
    # That determines the size of each box and the number of columns.
    # I use vw rather than vh to keep the boxes relatively squarish.
    # Also, did you just pronounce that as "vee-dubya"? I am disgusted.
    vw, columns = getColumns(colors)

    css_template = """body {{box-sizing: border-box}} h1 {{margin: 0em}} main {{display: grid; grid-template-columns: repeat({columns}, 1fr); grid-auto-rows: {vw}vw; grid-gap: 1em}} .colorbox {{padding: 1em; margin: 0.5em; overflow: visible}} p {{margin: 0em}}""".format(
        columns=columns,
        vw=vw
    )
    cssbox_template = "#{colorid} {{background-color: {colorvalue}; color: {borw}}}"
    html_header = ["<!DOCTYPE HTML>", """<html lang="zxx">""", "<head>",
                   """<meta charset="utf-8">""", title, "<style>", css_template]
    html_body = ["</style>", "</head>", "<body>", h1, "<main>"]
    html_close = ["</main>", "</body>", "</html>", ""]

    knownids = []
    knowncolors = []
    colorindex = 0
    for color in really_colors:
        colorid, colorvalue = color.split(": ")
        colorid = colorid[1:]
        # Add new colors.
        if colorid not in knownids:
            knownids.append(colorid)
            knowncolors.append(colorvalue)
            contrast = checkContrast(colorvalue)
            if contrast < 4.5:
                borw = "#ffffff"
            else:
                borw = "#000000"
            cssbox = cssbox_template.format(
                colorid=colorid,
                colorvalue=colorvalue,
                borw=borw
            )
            html = """<div class="colorbox" id="{colorid}"><p>{colorid}: {colorvalue}</p></div>""".format(
                colorid=colorid,
                colorvalue=colorvalue)
            c = {"colorid": colorid, "colorvalue": colorvalue,
                 "cssbox": cssbox, "html": html}
            html_header.append(cssbox)
            html_body.append(html)
        # GIMP palettes don't necessarily have unique color names,
        # so rename colors as needed to avoid overlap.
        elif colorid in knownids and colorvalue not in knowncolors:
            colorid = "{colorid}{colorindex}".format(
                colorid=colorid,
                colorindex=str(colorindex)
            )
            colorindex += 1
            contrast = checkContrast(colorvalue)
            if contrast < 4.5:
                borw = "#ffffff"
            else:
                borw = "#000000"
            cssbox = cssbox_template.format(
                colorid=colorid,
                colorvalue=colorvalue,
                borw=borw
            )
            html = """<div class="colorbox" id="{colorid}"><p>{colorid}: {colorvalue}</p></div>""".format(
                colorid=colorid,
                colorvalue=colorvalue
            )
            c = {"colorid": colorid, "colorvalue": colorvalue,
                 "cssbox": cssbox, "html": html}
            html_header.append(cssbox)
            html_body.append(html)

    all_html_elements = html_header + html_body + html_close
    html = "\n".join(all_html_elements)

    outname = "{noext}_palette.html".format(noext=sass_noext_safe)
    outpath = os.path.join(save_path, outname)
    with open(outpath, "w") as fout:
        fout.write(html)
    print("Wrote {outpath}.".format(outpath=outpath))

if __name__ == '__main__':
    main()
