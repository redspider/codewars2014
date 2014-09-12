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

03:02

The file contained a key in the form of a Letter -> Hex code, and a bunch of text at the bottom. Performing a replace
using the key resulted in an ASCII rendering of the solution.

We basically mangled this with our text editors to make the key trivial to parse and then did a quick substitution.

#### Question 2: Square Bits

16:35

> "We spent half the time waving our phones at invalid QR codes like complete muppets"

This was the closest we came to being genuinely stumped. The file contained 441 1s and 0s and the comment said "Almost
a Perfect Square". We initially guessed it needed to be in a square but rapid math and dodgy regex splitting meant
that we had one character left over some how. This led us to conclude it wasn't actually supposed to be a square for
a bit and we re-split (using regex in my case, a macro in Martyns) back to 7 per line and tried interpreting as 
ASCII but that didn't work.

Then Martyn put it back into a square again then turned his laptop top me and said "Can you go cross-eyed?". He'd noticed
that there was something of a pattern to the output, one that became pretty clear once we replaced the 0's and 1's with
things that were more obviously pixels. Still not sure what the cross-eyed bit was about tho.

It was a QR Code, all that we needed to do was interpret it. This was somewhat problematic, because it turns out QR Codes
 need to be kinda square, and because we were printing ours out on a terminal it was stretched downwards instead. We
 scrambled for various strategies to make it look right including using the unicode block character. First to find a
 solution was Martyn who took a screenshot of the terminal output and then squashed it using Gimp.
 
 Grant later pointed out we could have made it square just by printing two blocks or two spaces for each "pixel",
 which is far easier and is what I implemented in the reference solution.
 
 
#### Question 3: Russian Dolls

08:50

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

#### Question 4: Turtles all the way

09:25

Question 4 was a zip file containing a text file. The text file was a simple set of Turtle/LOGO instructions for drawing
an image. It turned out implementing the turtle was trivial, but we found ourselves suddenly stumped when we needed to
render the output - it was far too big to output as blocks on the terminal and stupidly none of us had thought to add
some kind of image library.

We attacked the problem from multiple directions but the winner on the day was Martyn with an enormous HTML file full of
ascii output surrounded in a pre tag and resized via css to one pixel each. This may have been the dirtiest hack we
implemented in the competition and we still feel shamed.

Next time I'll make sure I have PIL installed.

#### Question 5: Rock paper scissors

24:00
 
This one was interesting mostly because it was more of a programming problem than the previous questions. The file
contained a set of files containing moves for various players in a Rock Paper Scissors tournament. To find the solution
all you needed to do was implement a rock-paper-scissors knock-out tournament to figure out who won, and use the names
of the winner and the other finalist as the code.

Given that Nigel does getyourgameon.co.nz knockout tournaments were something of a specialty, we did two independent 
 solutions - Nigel and Martyn wrote a hack and I did something vaguely respectable.
 
We ran into one issue late in the day - it hadn't been clear from the instructions whether the set of moves started
again from the top each game, or whether the moves just kept getting consumed by each game played. We guessed the first
but it turned out to be the latter. This required some last minute rewriting of the hack but we got the solution.

#### Question 6: Oh god what I don't even

28:37

The final problem came in two parts, and the first part is notable primarily because we did possibly the least efficient
solution ever. In essence it consisted of a set of single-line PNGs in an HTML file. The task was to line the slices up
such that the red pixel near the start of each line matched up vertically, thus giving you the solution.

We could have done this any number of trivial ways, either by editing the HTML in the inspector to line it up using 
positions or pulling the images into an image editor. Instead we all did the dumb thing and started coding methods to
find the offsets - I don't even know why.
  
Martyn used xpm mode in vim to obtain the offsets as characters and called them out to Nigel who modified the HTML to
reflect those. This gave us the URL to the second part.

The second part was just mean. Grant, you're mean.

It involved an HTML "spreadsheet" in which a grid of numbers were displayed, and a "formula" input box. The formula
specified something like A4+G2, and we were required to put the answer into the answer box and submit.

The issue was that there was 100 of these back to back, and you had 5 seconds to answer each one or you had to go
back to the start. They were also somewhat randomly generated.

Again we split into two parts both aiming for a solution. There were two main tricks - first was parsing the HTML
itself to get the table. Using (in my case) lxml and .cssselect made this straightforward enough. But two main
barriers slowed us down a bit.

The first was somewhat unintentional - the website that was hosting the challenge had an invalid SSL certificate, and
every library we generally use to do this kind of thing gets really angry about those. It took a bit of time to bypass
those checks somehow.

The second was the interpretation of the formula itself. We took two different tracks on this - Nigel and Martyn went
with mangling it so it could be eval'd in perl and I started on a proper parser in case that turned out not to work. It
almost came down to my backup plan - around question 60 suddenly instead of pure math the formulas started using 
functions too - SQRT() and MAX(). Nigel and Martyn managed to work around that but if the formulas had become much more
complex it could have got ugly. Later after the match we theorised that a truly nasty Grant could have put "exit;" 
in a formula.

Finally we were approaching the solution. With one caveat - Martyn realised that he wasn't saving the output HTML
anywhere so when it hit 100 we wouldn't actually have the solution code. Fortunately mean Grant had decided to be
nice in this instance and output the code in the formula box so we got it anyway.

### Final notes

We had good fun doing the various problems and they felt like a good level of challenge. We are thoroughly embarrassed by
the code we wrote and hope it never sees the light of day. The reference solutions here are intended to redeem us to some
degree.


