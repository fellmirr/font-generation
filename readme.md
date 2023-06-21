A python program that takes in a font file, uses fonttools python package to strip most of the
characters from the font, and then outputs the font file in compressed woff2 format
Optionally the program will also output the font file as a base64 encoded string

Has arguments for which subset of font characters to use
The subsets txt files in the /charactersubsets folder

-s includes a set of commonly used symbols such as arrows
-l includes font ligatures for fi, fl, ff, ffi, ffl
-h includes a hack for some special greek letters that are used to display semibold numbers in a non-bold font

Usage: `python generate.py <font file> <output file> <flags (-s, -l, -h)> <optional: base64>`

Font files can be found on our google drive.