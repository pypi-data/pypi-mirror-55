import numpy as np

def alphabetize_concat(input_list):
    """
    Takes a python list.
    List can contain arbitrary objects with .__str__() method
        (so string, int, float are all ok.)
    Sorts them alphanumerically.
    Returns a single string with result joined by underscores.
    """
    array = np.array(input_list, dtype=str)
    array.sort()
    return '_'.join(array)
