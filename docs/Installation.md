# Installation

## General unix and Linux (OSX)

I have now installed gnuradio 5 different ways....

* Live USB - This is good but it is very difficult to get some newer machines to boot from it... will try and revert some notes in here, although I invite you to try yourself with lots of googling. It is a good way to really understand the EFI and security.

* apt-get - Generally not a great idea... versions can be out compared to current, reuses ppa's etc.

* build-gnuradio script - This is not too bad... some minor bugs in the script. However it is a good source to sometimes add your own bits in the right sequence.

* pybombs... this looks like a good idea... and it works , and it creates most of the environment in a "User" directory, so can be used to have multiple versions! However it can have minor troubles or missing dependencies and then it can be really tricky to debug.

* mac ports builds ....... my advice ... don't. The macports integration with the audio stack is a bit all over the shop, can be really slow, the process is easily 24 hours, and maintaing updates.... ok rule 1 here - update when you are ready to walk away from machine for hours (6-8).



The scripts here are using bash, curl, awk, gsed, sed, sort, ex, tr, perl (and probably some other bits) 

It was developed with the QAN (Quick and Nasty) principle over a couple of years, and finally got out of hand!

Note that despite this it runs in about 3 seconds on my mac (2.5 seconds is the curl get of files)

## Main plugins

hackrf
gr-fcdproplus

gr-osmosdr
gr-dsd


## scipts for setup

will go here
and some other bits

* I just run and have a quick look at errors until things are fixed up