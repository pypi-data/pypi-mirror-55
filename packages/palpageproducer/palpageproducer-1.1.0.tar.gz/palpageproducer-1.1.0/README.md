# Palette Page Producer

Input: a SASS stylesheet (.scss), a LESS stylesheet (.less), or a GIMP palette (.gpl).

Output: an HTML document with boxes of the colors defined in the input file (in `~/.local/share/palpageproducer/output` or the equivalent).

Dependencies:

+ [appdirs](https://pypi.org/project/appdirs/)
+ [awesome-slugify](https://pypi.org/project/awesome-slugify/)

----

I made this because I wanted an easy way to see what the colors in a webpage/game/etc. looked like together. Because Palette Page Producer also lists the variable names and hex codes of each color, it also makes it easy to copy a given value (e.g. to throw it into WebAIM's Color Contrast Checker).

Caveats:

+ PPP doesn't check if the output already exists before overwriting.
+ LESS files aren't as well-tested as the other formats yet and may have strange errors.
+ The output uses some fancy CSS features (like `grid` and `vw`) that not all browsers support.
+ RGB palette colors are converted to hex output. RGBA colors are ignored entirely.
+ If color I.D.s are duplicated (e.g. a GIMP palette with multiple colors named "Untitled"), PPP automatically appends a number to the I.D. to avoid overlap problems. This means that the I.D.s seen in the output may not match to the originals 100%.
+ The output uses a `<style>` element in the `<head>`, rather than creating two separate (.HTML and .CSS) files. Some linters don't like `<style>` tags under any circumstances, so you may get false "invalid" results, but the output is indeed valid HTML5.

I'd like to eventually add command line options to specify column count and output filename, but those aren't available yet.