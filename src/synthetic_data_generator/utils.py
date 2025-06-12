import warnings
import random
import numpy as np


def create_weighted_generator(max_number, max_ceiling=None, start=4, weight_range=(7, 11), weight_multiplier=3):
    """
    Creates a weighted random generator for range [start, max_number]
    with higher weights for numbers in weight_range.
    """
    if max_number < start:
        raise ValueError(f"max_number ({max_number}) must be >= start ({start})")
    
    # Set a max range
    if max_ceiling:
        if max_number > max_ceiling:
            max_number = max_ceiling

    # Create the range
    numbers = np.arange(start, max_number + 1)
    
    # Create weights - start with all 1s
    weights = np.ones(len(numbers))
    
    # Find indices within the weight range that also exist in our number range
    weight_min, weight_max = weight_range
    if weight_max >= max_number:
        weight_max = max_number
        warnings.warn("max range set equal to book's chapters number ", category=UserWarning)
    mask = (numbers > weight_min) & (numbers <= weight_max)
    weights[mask] = weight_multiplier
    
    # Normalize weights
    weights = weights / weights.sum()
    
    return int(np.random.choice(numbers, p=weights))


def add_random_spacing(range=range(1,5), weights=[.6,.2,.1,.1]):
    """ add spacing with random size"""
    n_spaces = random.choices(range, weights=weights, k=1)[0]
    spacing = " " * n_spaces
    return spacing