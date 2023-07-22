from PyQt5.QtCore import Qt


def traverse_items(item, parameter_list):
    for row in range(item.rowCount()):
            child_item = item.child(row)
            parameter_attributes = child_item.data(Qt.UserRole)
            if parameter_attributes is not None:
                if parameter_attributes.get('is_catalog', 0) == 0:
                    parameter_list.append(child_item)
            if child_item is not None:
                traverse_items(child_item, parameter_list)
