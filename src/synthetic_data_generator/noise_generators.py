import random
import string
import numpy as np
from utils import add_random_spacing


# =======================
# === Systemic Noise ===
# =======================

def generate_systemic_noise_layout():
    """Generates a layout for systemic noise in a book."""
    # section noise
    number_sections = random.choices([1,2,3], weights=[.5,.35,.15], k=1)[0] 
    text_sections_noise = ["Exercises", "References",  "Bibliography", "Notes", "Further Reading", "Contents", "Tables"]
    text_sections_weights = [0.3, 0.2, 0.2, 0.1, 0.1, 0.05, .05]
    text_section = np.random.choice(
                                    text_sections_noise,
                                    size=number_sections,
                                    replace=False,  
                                    p=text_sections_weights
    )

    # add numbers to sections
    add_numbers = random.choices([0,1], weights=[.7,.3], k=number_sections)
    
    return {
        "text_section": text_section,
        "add_numbers": add_numbers
    }
    
    
def format_systemic_noise(noise_layout, start_page, end_page, toc_noise):
    """Formats a chapter using the given book layout."""
    add_random_noise = random.choices([0,1], weights=[.7,.3], k=1)[0]
    if add_random_noise:
        random_noise = str(np.random.choice(toc_noise, 1, replace=False)[0])
        random_noise_position = random.randint(0, len(noise_layout['text_section']))
    
    noise_output = ""
    current_number = ""

    for idx, _ in enumerate(noise_layout['text_section']):
        # get random noise
        if add_random_noise and idx == random_noise_position:
            noise_output += add_random_spacing() + random_noise + "\n"
        
        # get numbers to add
        if noise_layout['add_numbers'][idx]:
            try:
                if not current_number:
                    number_to_add = random.sample(range(start_page,end_page-2), 1)[0]
                else:
                    number_to_add = random.sample(range(start_page,end_page), 1)[0]
            except:
                number_to_add = ""
            current_number = number_to_add
        else:
            current_number = ""

        # define noise output
        noise_output += noise_layout['text_section'][idx] + add_random_spacing() + str(current_number) + "\n"
        
    return noise_output


# =======================
# === Random Noise ===
# =======================

def generate_symbol_noise(min_len=1, max_len=3):
    """Generate random symbols and punctuation"""
    length = random.randint(min_len, max_len)
    symbols = "!@#$%^&*()[]{}|;:,.<>?/~`_+-="
    return ''.join(random.choices(symbols, k=length))


def generate_number_noise(min_digits=1, max_digits=4):
    """Generate random number strings"""
    length = random.randint(min_digits, max_digits)
    return ''.join(random.choices(string.digits, k=length))


def generate_page_number_noise():
    """Generate realistic but random page number patterns"""
    patterns = [
        f"Page {random.randint(1, 999)}",
        f"p. {random.randint(1, 999)}",
        f"pp. {random.randint(1, 999)}-{random.randint(1, 999)}",
        f"{random.randint(1, 999)}",
        f"[{random.randint(1, 999)}]",
        f"({random.randint(1, 999)})",
    ]
    return random.choice(patterns)


def generate_formatting_noise():
    """Generate random formatting-like text"""
    formats = [
        "...............",
        "_______________",
        "---------------",
        "===============",
        "***************",
        "###############",
        "|||||||||||||||",
        "               ",  # spaces
        "\t\t\t\t",       # tabs
        "• • • • • • • •",
        "→ → → → → → →",
        "※ ※ ※ ※ ※ ※",
    ]
    return random.choice(formats)


def generate_text_noise(toc_noise):
    """Sample random text from toc noise"""
    random_toc = str(np.random.choice(toc_noise, 1, replace=False)[0])
    words = random_toc.split()
    n_words = len(words)
    n_words_to_use = random.randint(1,n_words)
    words_ids = np.random.choice(range(0,n_words),n_words_to_use,replace=False)
    words_subset = ' '.join([words[idx] for idx in words_ids])
    return words_subset


def generate_random_noise(chunk_type="symbols", toc_noise=None):
    """Generate random noise based on the specified chunk type."""
    
    if chunk_type == "random":
        chunk_type = random.choice([
            "symbols", "numbers", "page_numbers", "formatting", "text"
        ])

    if chunk_type == "subchapters":
        chunk_type = random.choice([
            "symbols", "numbers", "text"
        ])
    
    generators = {
        "symbols": lambda: generate_symbol_noise(),
        "numbers": lambda: generate_number_noise(),
        "page_numbers": lambda: generate_page_number_noise(),
        "formatting": lambda: generate_formatting_noise(),
        "text": lambda: generate_text_noise(toc_noise)
    }
    
    return str(generators[chunk_type]())