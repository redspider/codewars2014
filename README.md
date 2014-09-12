## Code Wars 2014 reference solutions and comments

On the 21th of September, 2014 myself, Martyn and Nigel participated in the Kiwi Pycon Code Wars challenge as team Cats.
 
Code Wars involved a set of six problems, each represented by a single data file. The teams were required to solve each
 problem in order and obtain from the file an 8 letter ascii code which would allow them to unlock the next file. While
 it was a timed race against all the other teams the emphasis was primarily on fun.
 
This repository contains the problem set, and reference solutions to some of the problems that I ended up writing for
interest. Additionally comments on roughly how we actually solved each problem in the night are outlined below.

### Solutions on the night

The strategies used on the night don't remotely resemble those implemented in the solutions here. Mostly this is 
because you're never quite certain what you're looking for, so you're always looking for the simplest way to find out
if you're on the right track.


#### Question 1: Key and Ciphertext

The file contained a key in the form of a Letter -> Hex code, and a bunch of text at the bottom. Performing a replace
using the key resulted in an ASCII rendering of the solution.

We basically mangled this with our text editors to make the key trivial to parse and then did a quick substitution.

#### Question 2: Square Bits

This was the closest we came to being genuinely stumped. The file contained 441 1s and 0s and the comment said "Almost
a Perfect Square". We initially guessed it needed to be in a square but rapid math and dodgy regex splitting meant
that we had one character left over some how. This led us to conclude it wasn't actually supposed to be a square for
a bit and we re-split (using regex in my case, a macro in Martyns) back to 7 per line and tried interpreting as 
ASCII but that didn't work.

Then Martyn put it back into a square again then turned his laptop top me and said "Can you go cross-eyed?". He'd noticed
that there was something of a pattern to the output, oen that became pretty clear once we replaced the 0's and 1's with
things that were more obviously pixels.

It was a QR Code, all that we needed to do was interpret it. This was somewhat problematic, because it turns out QR Codes
 need to be kinda square, and because we were printing ours out on a terminal it was stretched downwards instead. We
 scrambled for various strategies to make it look right including using the unicode block character. First to find a
 solution was Martyn who took a screenshot of the terminal output and then squashed it using Gimp.
 
#### Question 3: Russian Dolls

This one was mostly straightforward - the file started off uuencoded, which contained a gzipped text file containing a
hex dump of a zip file containing 27 individual PDF files consisting of a base64'd PNG file, inside the data block of
which was embedded a riddle to come up with the solution.
   
Each of the "russian doll" of file formats was pretty simple, we just used the shell command "file" liberally until we
hit the hex dump. We used "xxd -r" to change the hex dump into the zip file, then we hit the PDF files.

We split into two teams with that - two of us started copy/pasting the text into text files, Martyn went for automation
and got a solution to pull the text. In fact that was less annoying than trying to reassemble the pages into the right
order - the use of english words for numbers doesn't have a trivial solution without finding some kind of library,
but there were only 27 of them so we renamed them manually.

We got the PNG, then out of little more than habit I ran "strings" on it and sure enough there was some text embedded 
in there. The riddle basically said the solution was the date of the moon landing in ISO date format.

