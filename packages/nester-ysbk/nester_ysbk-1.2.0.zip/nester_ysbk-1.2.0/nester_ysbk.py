def print_lol(this_list, level=0):
    for each_item in this_list:
        if isinstance(each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_stop in range(level):
#python3语法                print("\t", end='')
                print " ",
            print(each_item)
