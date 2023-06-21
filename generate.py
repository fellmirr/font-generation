'''
A python program that takes in a font file, uses fonttools python package to strip most of the
characters from the font, and then outputs the font file in compressed woff2 format
Optionally the program will also output the font file as a base64 encoded string

Has arguments for which subset of font characters to use
The subsets txt files in the /charactersubsets folder

-s includes a set of commonly used symbols such as arrows
-l includes font ligatures for fi, fl, ff, ffi, ffl
-h includes a hack for some special greek letters that are used to display semibold numbers in a non-bold font

Usage: python generate.py <font file> <output file> <optional: base64>
'''

# Imports
import os
import sys
import base64

# Constants
# The font file to use
FONT_FILE = sys.argv[1]
# The output file to write to
OUTPUT_FILE = sys.argv[2]
# Whether to output the font as a base64 encoded string
BASE64 = sys.argv[-1] == 'base64'

# The character subsets to use
# The default subset is the basic characters used in Norwegian and Swedish
CHARACTER_SUBSETS = ['bodycharacters']
# If the -s argument is given, include a set of commonly used symbols such as arrows
if '-s' in sys.argv:
    CHARACTER_SUBSETS.append('commonsymbols')
# If the -l argument is given, include font ligatures for fi, fl, ff, ffi, ffl
if '-l' in sys.argv:
    CHARACTER_SUBSETS.append('ligatures')
# If the -h argument is given, include a hack for some special greek letters that are used to display semibold numbers in a non-bold font
if '-h' in sys.argv:
    CHARACTER_SUBSETS.append('semiboldletterhack')

# Call pyftsubset to generate the font file

# Read all the character subset into a temporary txt file
unicodes = ''
for subset in CHARACTER_SUBSETS:
    with open('charactersubsets/' + subset + '.txt', 'r') as f:
        unicodes += f.read()

file = open('unicodes.txt', 'w')
file.write(unicodes)
file.close()

# Experiment with different settings for smaller fonts
commands = [
    'pyftsubset fonts/' + FONT_FILE + ' --output-file=output/' + OUTPUT_FILE + '.woff2 --flavor=woff2 --layout-features="*" --text-file=unicodes.txt',
    'pyftsubset fonts/' + FONT_FILE + ' --output-file=output/' + OUTPUT_FILE + '.woff2 --flavor=woff2 --layout-features="*" --text-file=unicodes.txt --desubroutinize',
    #'pyftsubset fonts/' + FONT_FILE + ' --output-file=output/' + OUTPUT_FILE + '.woff2 --flavor=woff2 --layout-features="*" --text-file=unicodes.txt --no-hinting --desubroutinize',
    'pyftsubset fonts/' + FONT_FILE + ' --output-file=output/' + OUTPUT_FILE + '.woff2 --flavor=woff2 --layout-features="*" --text-file=unicodes.txt --with-zopfli',
    'pyftsubset fonts/' + FONT_FILE + ' --output-file=output/' + OUTPUT_FILE + '.woff2 --flavor=woff2 --layout-features="*" --text-file=unicodes.txt --with-zopfli --desubroutinize',
    'pyftsubset fonts/' + FONT_FILE + ' --output-file=output/' + OUTPUT_FILE + '.woff2 --flavor=woff2 --layout-features="*" --text-file=unicodes.txt --no-notdef-glyph',
    'pyftsubset fonts/' + FONT_FILE + ' --output-file=output/' + OUTPUT_FILE + '.woff2 --flavor=woff2 --layout-features="*" --text-file=unicodes.txt --no-notdef-glyph --desubroutinize --no-layout-closure',
]

base64_results = []

for command in commands:
    # Run the command
    # print('Running command: ' + command)
    result = os.system(command)

    # If the command failed, print an error message and exit
    if result != 0:
        print('\033[91m' + 'Error: pyftsubset failed' + '\033[0m')
        continue

    # If the base64 argument is given, output the font as a base64 encoded string
    if BASE64:
        with open('output/' + OUTPUT_FILE + '.woff2', 'rb') as f:
            base64string = base64.b64encode(f.read()).decode('utf-8')
            # Print the length in bytes of the base64 string in red color
            base64_results.append({
                'command': command,
                'length': len(base64string),
                'base64string': base64string
            })

# Order base64 results by length, print command and length in bytes
base64_results.sort(key=lambda x: x['length'])
for result in base64_results:
    # Print command in yellow
    print('\033[93m' + result['command'] + '\033[0m')
    # Print length in red
    print('\033[91m' + str(result['length']) + ' bytes' + '\033[0m')

# Print the base 64 strings in green
for result in base64_results:
    # Print the ranking in green
    print()
    print('\033[92m' + str(base64_results.index(result) + 1) + '. best string \033[0m')
    print(result['base64string'])

# Delete the temporary txt file
os.remove('unicodes.txt')

