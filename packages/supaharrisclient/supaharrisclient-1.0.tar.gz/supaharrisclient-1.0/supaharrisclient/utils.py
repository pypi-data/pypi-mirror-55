import os
import sys
import json
from contextlib import contextmanager


def response_to_json(response):
    return json.loads(response.content.decode("utf8"))


def print_progressbar(i, N, whitespace=""):
    pbwidth = 42

    progress = float(i)/(N-1)
    block = int(round(pbwidth*progress))
    text = "\r{0}Progress: [{1}] {2:.1f}%".format(whitespace,
        "#"*block + "-"*(pbwidth-block), progress*100)
    sys.stdout.write(text)
    sys.stdout.flush()

    if i == (N-1):
        print(" .. done")


@contextmanager
def suppress_stdout():
    try:
        import numpy
        HAS_NUMPY = True
    except ImportError:
        HAS_NUMPY = False
    with open(os.devnull, "w") as devnull:
        if HAS_NUMPY: old_settings = numpy.seterr(all="ignore")
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            if HAS_NUMPY: numpy.seterr(**old_settings)
