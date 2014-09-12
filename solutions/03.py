#!env python
"""
Solution to problem 3 of the Kiwi Pycon 2014 Code Wars.


Technically this one doesn't really need a great deal of programming. It is primarily a matter of figuring out the
container in what amounts to a russian doll of file formats:

1. uuencoded
2. gzipped
3. hex-dumped (wtf grant)
4. Zipped
5. encoded into a bunch of PDFs (oh man)
6. base64 encoded
7. hidden as text inside a PNG


"""
import base64
from binascii import unhexlify
import re

import uu
import gzip
import shutil
import zipfile

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def pdf_to_text(s):
    # We use pdfminer to grab the content of the PDF because we're too lazy to do it ourselves.
    result = StringIO()
    interpreter = PDFPageInterpreter(PDFResourceManager(), TextConverter(PDFResourceManager(), result, codec='utf-8', laparams=LAParams()))
    for page in PDFPage.get_pages(StringIO(s)):
        interpreter.process_page(page)
    return result.getvalue()
"""
# Make a copy
shutil.copy('../problems/03-mooooon', '../tmp/03-uuencoded')

# UUDecode into the gzip
uu.decode('../tmp/03-uuencoded', '../tmp/03-gzipped.gz')

# Grab the gunzipped content
hexdump = gzip.open('../tmp/03-gzipped.gz').read()

# De-hexdumpify
content = unhexlify(''.join(re.findall(r' ([a-f0-9]{4})', hexdump)))
open('../tmp/03-zipped.zip', 'w').write(content)
"""
# Grab zip contents
zf = zipfile.ZipFile('../tmp/03-zipped.zip', 'r')
filenames = zf.namelist()

# We have to sort the files into the right order so that we can pull the data correctly. There are a few nicer ways of
# doing this using external mods like inflect but we'll keep things simple
NUMBERS = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve',
           'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty', 'twenty-one',
           'twenty-two', 'twenty-three', 'twenty-four', 'twenty-five', 'twenty-six', 'twenty-seven']

# Use string offsets to chop the string up to the number matches
filenames.sort(lambda a, b: cmp(NUMBERS.index(a[11:-4]), NUMBERS.index(b[11:-4])))

# Now we have them in order, open each PDF and read the content
base64_content = ""
for filename in filenames:
    base64_content += pdf_to_text(zf.open(filename).read())

# It's a PNG, but actually the info we want is hidden inside as text
clutter = base64.b64decode(base64_content)
for line in clutter.split('\n'):
    # Grab the matching lines - honestly this would be better done as a filter on the high ascii bit
    if not re.search(r'[\x7f-\xff]', line):
        print line

# The output is a riddle, asking for the ISO date of the first human being on the moon. 21 July 1969, gives us:
# 19690621
