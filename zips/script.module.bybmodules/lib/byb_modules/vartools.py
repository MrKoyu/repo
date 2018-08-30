


def dict_item_counter(List,item,match,match_type):
    #match_type 0 = excact match  1 = close match string is in string
    counter_list = [0]
    if match_type == 0:
        for items in List:
            item_to_check = items[item]
            if item_to_check == match:
                counter_list.append(1)
    if match_type == 1:
        for items in List:
            item_to_check = items[item]
            if match.lower().replace(' ','') in item_to_check.lower().replace(' ',''):
                counter_list.append(1)
    counter = sum(counter_list)
    return counter