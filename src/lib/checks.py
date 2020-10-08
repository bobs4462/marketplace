import sys

# Make sure that python version is above 3.5
def version_check():
    if (sys.version_info[0] + sys.version_info[1] / 10) < 3.6:  # Ugly, isn't it?
        raise Exception("Must be using Python 3.5 or newer")
