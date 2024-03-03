def remove_items_from_list(my_list_to_be_purged, index_nr_to_purge):
    # are they lists?
    if not isinstance(my_list_to_be_purged, list) or not isinstance(index_nr_to_purge, list):
        print('one of the inputs is not a list. Exiting function.')
        return  # Exits the function if the condition is met

    # remove all items from list that are not integers (no negative indices allowed)
    org_index_nr_to_purge = index_nr_to_purge
    index_nr_to_purge = [index for index in index_nr_to_purge if isinstance(index, int) and index > 0]
    if org_index_nr_to_purge != index_nr_to_purge:
        print('contents  of indices list corrected to contain only positive integers')

    # make sure list has only uniqe items
    old_index_list1 = index_nr_to_purge
    index_nr_to_purge = list(set(index_nr_to_purge))
    if old_index_list1 != index_nr_to_purge:
        print('removed duplicates on indices list')

    length_of_my_list_to_be_purged = len(my_list_to_be_purged)
    length_of_indices_to_purge = len(index_nr_to_purge)

    # number of indices to remove must be lower than length of the list

    if length_of_my_list_to_be_purged < length_of_indices_to_purge:
        print('cannot remove more indexes than my_list items count')
        return


   # purged_list = my_list_to_be_purged

    for index in sorted(index_nr_to_purge, reverse=True):
        my_list_to_be_purged.pop(index)

    return my_list_to_be_purged


def print_results(test_set, my_list, indices):
    print(f'\n\ntest_set {test_set} \n')

    my_list_to_be_purged = my_list
    index_nr_to_purge = indices
    print('list: (', len(my_list_to_be_purged), ') ', my_list_to_be_purged)
    print('indices: (', len(index_nr_to_purge), ') ', index_nr_to_purge)

    purged_list = remove_items_from_list(my_list_to_be_purged, index_nr_to_purge)
    print('resulting list:', purged_list)
    print('\n ---------------------------------')

    return


test_set = 0
my_list_to_be_purged = [21, 22, 23, 24, 25, 26, 27, 28, 29, "aa"]
index_nr_to_purge = '[1,2,3]'
print_results(test_set, my_list_to_be_purged, index_nr_to_purge)

test_set = 1
my_list_to_be_purged = [21, 22, 23, 24, 25, 26, 27, 28, 29, "aa"]
index_nr_to_purge = [1, 'a', 3, -4]
print_results(test_set, my_list_to_be_purged, index_nr_to_purge)

test_set = 2
my_list_to_be_purged = [21, 22, 23, 24, 25, 26, 27, 28, 29, "aa"]
index_nr_to_purge = [1, 2, 4, 4, 1]
print_results(test_set, my_list_to_be_purged, index_nr_to_purge)

test_set = 3
my_list_to_be_purged = [21, 22, 23]
index_nr_to_purge = [1, 2, 3, 4]
print_results(test_set, my_list_to_be_purged, index_nr_to_purge)
