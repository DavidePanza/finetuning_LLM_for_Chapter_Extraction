import numpy as np
from utils import add_random_spacing


def format_subchapter(text, sub_number, sub_page, use_numbers, use_pages):
    """Generates a consistent layout for all suchapters in a book."""
    if not use_numbers and not use_pages:
        return f"{add_random_spacing(range=range(0,3), weights=[.7,.2,.1])}{text}\n"
    elif use_numbers and not use_pages:
        return f"{add_random_spacing(range=range(0,3), weights=[.7,.2,.1])}{str(sub_number)} {text}\n"
    elif not use_numbers and use_pages:
        return f"{text}{add_random_spacing(range=range(1,4), weights=[.6,.2,.6])}{str(sub_page)}\n"
    else:
        return f"{add_random_spacing(range=range(0,3), weights=[.85,.1,.05])}{str(sub_number)} {text}{add_random_spacing(range=range(1,4), weights=[.7,.2,.1])}{str(sub_page)}\n"
