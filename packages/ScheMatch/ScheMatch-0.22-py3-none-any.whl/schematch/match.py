def are_keys_same_in_dictionary(dictionary_one, dictionary_two):
    if (type(dictionary_one) is not dict) or (type(dictionary_two) is not dict):
        return (False, "One of the inputs is not dictionary")
    else:
        if len(dictionary_one.keys()) != len(dictionary_two.keys()):
            return (False, "Number of keys different in dictionaries")
        for k in dictionary_one.keys():
            if k in dictionary_two.keys():
                if (type(dictionary_one[k]) == dict):
                    is_inner_dic_same = are_keys_same_in_dictionary(
                        dictionary_one[k], dictionary_two[k])
                    if is_inner_dic_same[0] == False:
                        return is_inner_dic_same
            else:
                return (False, "The key " + k + " not found in second dictionary")
    return (True, "")
