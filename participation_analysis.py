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

# First, import from __future__ so our code will run on both Python 2 and 3
from __future__ import division, print_function
import os
import pandas as pd
import matplotlib.pyplot as plt

# Try to import Seaborn to make plots pretty
try:
    import seaborn
    seaborn.set(style="white", context="notebook", font_scale=1.5)
except ImportError:
    print("Cannot import Seaborn. Try:\n\n    conda install seaborn\n")


def correct_department(dept_name):
    """
    Correct department names so there aren't apparent duplicates.
    """
    # Create a dictionary for department aliases that we can look up
    aliases = {"OE": "Ocean Engineering",
               "ME": "Mechanical Engineering",
               "Earth Science": "Earth Sciences",
               "EOS": "Earth Sciences",
               "OPAL": "Earth Sciences"}
    # Add some rules for fixing department names
    if dept_name in aliases.keys():
        return aliases[dept_name]
    elif " ".join(dept_name.split()[:2]) in aliases.keys():
        return aliases[" ".join(dept_name.split()[:2])]
    elif "oceanog" in dept_name.lower():
        return "Earth Sciences"
    elif "civil" in dept_name.lower():
        return "Civil Engineering"
    elif dept_name.isupper():
        return dept_name
    else:
        # Return the name formetted with title case
        return dept_name.title()

def correct_title(title):
    """
    Return properly formatted job title.
    """
    # Make sure title is a string
    title = str(title)
    if "grad student" in title.lower():
        return "Grad student"
    # We will group all professors together
    if "professor" in title.lower():
        return "Professor"
    else:
        return "Research staff"
    
def test_correct_title():
    assert correct_title("Scientific Data Analyst") == "Research staff"
    assert correct_title("Research scientist") == "Research staff"
    assert correct_title("Grad student") == "Grad student"
    assert correct_title("Bob Johnson Professor of Awesome Stuff") \
            == "Professor"
    print("Passed")


def load_data(time="interested", quantity="department"):
    """
    Load CSV data from a specified time in 
    `["interested", "registered", "signin_day1", "signin_day2"]`
    then correct names and return a Series with value counts for the 
    specified quantity.
    """
    # Create a file name using Python's new style string formatting
    fname = "data/anonymized/{}_{}.csv".format(time, quantity)
    # Load CSV data using Pandas
    df = pd.read_csv(fname)
    # Correct department name
    if quantity == "department":
        df.department = [correct_department(d) for d in df.department]
    # Correct job title
    elif quantity == "title":
        df.title = [correct_title(t) for t in df.title]
    return df[quantity].value_counts()
            
def load_all_times(quantity="department"):
    """
    Loads data for a specified quantity over all times.
    """
    # Create empty DataFrame
    df = pd.DataFrame()
    for time, timename in [("interested","Interested"), 
                           ("registered", "Registered"),
                           ("signin_day1", "Signed-in day 1"),
                           ("signin_day2", "Signed-in day 2")]:
        df[timename] = load_data(time, quantity)
    df.index.name = quantity.title()
    # Replace NaNs with zeros since these are counts
    df = df.fillna(0)
    return df

def plot_all_times(quantity="department", save=False, savetype=".png"):
    """
    Loads data for all time for specified quantity into a DataFrame, then 
    creates a stacked bar chart from these. 
    """
    df = load_all_times(quantity)
    fig, ax = plt.subplots(figsize=(9, 5))
    df.transpose().plot(ax=ax, kind="bar", stacked=True, rot=0)
    ax.set_ylabel("Number of people")
    legend = ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    if save:
        if not os.path.isdir("figures"):
            os.mkdir("figures")
        fname = os.path.join("figures", quantity + savetype)
        fig.savefig(fname, bbox_extra_artists=(legend,), bbox_inches="tight")

if __name__ == "__main__":
    print("Testing correct_title function")
    test_correct_title()
    
    plot_all_times("department", save=True, savetype=".png")
    plot_all_times("title", save=True, savetype=".png")
    plt.show()

