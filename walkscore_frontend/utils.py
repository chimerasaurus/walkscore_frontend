def merge_dicts(*dicts):
    """Merge dictionaries together."""
    return_dict = dict()
    for d in dicts:
        return_dict.update(d)
    return return_dict
    
def remove_unneeded_elements(dict_to_clean, attrs_to_remove):
    """Pop unneeded elements from the given dictionary."""
    for key in attrs_to_remove:
        dict_to_clean.pop(key)
    return dict_to_clean