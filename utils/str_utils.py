def make_stringlist_from_list(list):
    i=0
    str_obj=str()
    for field in list:
        if i == 0:
            str_obj = str_obj+f'{field}'
        else:
            str_obj = str_obj+f',{field}'
        i+=1
    return str_obj
