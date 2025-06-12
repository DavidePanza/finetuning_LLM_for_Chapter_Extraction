import random
from utils import add_random_spacing


def generate_chapter_layout():
    """Generates a consistent layout for all chapters in a book."""
    layout_types = [
        "Chapter {}: ",  # "Chapter 1: "
        "{}. ",          # "1. "
        "{} ",           # "1 "
        "chapter {} ",   # "chapter 1 "
        "Chapter {} "    # "Chapter 1 "
    ]
    weights = [0.1, 0.4, 0.4, 0.05, 0.05]
    number_layout = random.choices(layout_types, weights=weights, k=1)[0]
    
    nextline_page_number = random.choices([1, 0], weights=[0.15, 0.85], k=1)[0]

    return {
        "number_layout": number_layout,
        "nextline_page_number": nextline_page_number
    }


def format_chapter(layout, title, number, page_start):
    """Formats a chapter using the given book layout."""
    if layout["nextline_page_number"]:
        page_start = f"\n{add_random_spacing(range=range(0,6), weights=[.5,.2,.1,.1,.05,.05])}{page_start}"
    else:
        page_start = f"{add_random_spacing(range=range(1,7), weights=[.5,.2,.1,.1,.05,.05])}{page_start}"
    
    return f"{layout['number_layout'].format(number)}{title}{page_start}"