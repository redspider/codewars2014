#!env python
"""
Solution to problem 2 of the Kiwi Pycon 2014 Code Wars.

In this problem we are provided with a context-free bunch of binary. It turns out this is a QR Code if you render it
right. We take a simple approach in this case by replacing 1's with two full-block unicode characters, and 0's with
two spaces. We use two in order to ensure the QR Code is roughly square, if you use one you end up with a kinda squished
one and the readers don't like it.

We could also have implemented the qr decode algorithm directly but everyone has phones that read these things these
days, and it's not entirely straightforward.
"""
import re

bits = open('../problems/02-square-bits', 'r').read()

# Add in line-feeds
bits = re.sub(r'(.{21})','\\1\n', bits)

# Replace 0's with two spaces, 1's with two boxes
bits = bits.replace('0', '  ')
bits = bits.replace('1', u"\u2588"*2)

# Dump it out
print bits
