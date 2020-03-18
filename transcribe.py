from g2p_en import G2p
import string
import re
import glob
import os
import re

g2p = G2p()


def transcribe_to_phonemes(raw_lyrics):
    raw_lyrics = raw_lyrics.splitlines()

    lyrics = [g2p(line.translate(str.maketrans('', '', string.punctuation))) + ['<l>']
              for line in raw_lyrics if line != '']
    lyrics = [['<b>' if x == ' ' else x for x in line]
              for line in lyrics]
    lyrics = [word for line in lyrics for word in line]

    lyrics = " ".join(lyrics)

    return lyrics
