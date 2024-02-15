
def param_convert_tree_to_list(item):
    params_list = list()
    convert_tree_branch_to_list(item, params_list)
    return params_list

def convert_tree_branch_to_list(item, params_list: list):
    param_attributes = item.get_param_attributes()
    if param_attributes.get('is_catalog', 0) == 1:
        row_count = item.rowCount()
        for row in range(row_count):
            child_item = item.child(row)
            convert_tree_branch_to_list(child_item, params_list)
    else:
        params_list.append(item)
