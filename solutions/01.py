#!env python
"""
Solution to problem 1 of the Kiwi Pycon 2014 Code Wars.

In this case we're looking at a substitution cipher with a provided key. Interestingly the output is an ASCII
drawing of the relevant text, not the text itself.
"""

import re
from string import maketrans

# Grab the file, split into cipher key / value and plaintext

keys = ""
values = ""
ciphertext = ""

for line in open('../problems/01-cipher', 'r'):
    m = re.search(r'\| (\S) \| (\S\S) ', line)
    if m:
        keys += m.group(1)
        values += chr(int(m.group(2), 16))
    elif re.search(r'\w+', line):
        ciphertext += line

# Perform substitution. Effectively we are replacing each character in keys with the same index in values, ignoring
# anything else.
table = maketrans(keys, values)
print ciphertext.translate(table)
