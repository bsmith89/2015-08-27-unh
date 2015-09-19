#!/usr/bin/env python
"""
Python script version of the `feedback_analysis.ipynb` notebook

This was generated with 

    ipython nbconvert feedback_analysis.ipynb --to python

Comments were removed and top-level functions calls were moved to the end.

Note that the `if __name__ == "__main__":` statment at the end tells Python
what to do if this is run as a script versus imported as a module to use in
another script.
"""

from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
from PIL import Image


def load_text():
    """
    Load text, omitting lines beginning with "#" and removing words in 
    brackets.
    """
    text = ""
    with open("data/feedback_positive.txt") as f:
        for line in f:
            if not line.strip().startswith("#") and len(line.strip()) > 0:
                text += line
    text = re.sub(r"\[.*?\]", "", text)
    return text

if __name__ == "__main__":
    text = load_text()

    logos_mask = np.array(Image.open("images/logos.png"))

    wc = WordCloud(background_color="white", max_words=20000, mask=logos_mask)
    # Renerate word cloud
    wc.generate(text)

    # Store to file
    wc.to_file("images/wordcloud_raw.png")

    # Get the size of the image
    size_pixels = np.array(logos_mask.shape[:-1])
    dpi = 60
    size_inches = size_pixels/dpi

    # Show the wordcloud with matplotlib
    plt.figure(figsize=size_inches)
    plt.imshow(wc)
    plt.axis("off")

    background = Image.open("images/logos.png").convert("RGBA")
    wordcloud = Image.open("images/wordcloud_raw.png").convert("RGBA")
    blended = Image.blend(wordcloud, background, 0.1)
    blended.save("images/unh_swc_wordcloud.png", "PNG")

    # Show the new blended image with matlotlib
    plt.figure(figsize=size_inches)
    plt.imshow(blended)
    plt.axis("off")
    plt.show()
