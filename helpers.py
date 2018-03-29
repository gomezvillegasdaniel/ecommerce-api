
def clean_dict_by_none_values(d):
    return {k: v for k, v in d.items() if v != None}
