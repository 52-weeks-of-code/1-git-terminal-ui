import msvcrt


def manage_input(key, state):
    if state['input_mode'] == "navigation":
        if key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                state['direction'] = "up"
            elif key == b'K':
                state['direction'] = "left"
            elif key == b'M':
                state['direction'] = "right"
            elif key == b'P':
                state['direction'] = "down"
            else: 
                state['direction'] = 'None'
                
            update_focus_table(focus_table=state['focus_table'], direction=state['direction'])

        
        elif key == b'\r':
            state['input_mode'] = "focused"

    elif state['input_mode'] == "focused":
        if key == b'\x1b':
            state['input_mode'] = "navigation"

        if state['focus_table'][0][0]:
            pass

        elif state['focus_table'][0][1]:
            pass

        elif state['focus_table'][0][2]:
            pass

        elif state['focus_table'][1][0]:
            pass
        
        elif state['focus_table'][1][1]:
            pass




def update_focus_table(focus_table, direction):
    current_focus_col = None
    current_focus_col_index = None
    current_focus_row_index = None

    for index, col in enumerate(focus_table):
        if 1 in col:
            current_focus_col = col
            current_focus_col_index = index
            continue
    
    for index, value in enumerate(current_focus_col):
        if value == 1:
            current_focus_row_index = index
            continue

    if (direction == 'down' or direction == "up"):
        if direction == 'down':
            to_add = 1
        else:
            to_add = -1
        new_focus_col_index = current_focus_col_index
        new_focus_row_index = (current_focus_row_index + to_add) % len(focus_table[new_focus_col_index])

        focus_table[current_focus_col_index][current_focus_row_index] = 0
        focus_table[new_focus_col_index][new_focus_row_index] = 1
    

    elif (direction == "left" or direction == "right"):
        if direction == "left":
            to_add = 1
        else: 
            to_add = -1

        new_focus_col_index = (current_focus_col_index + to_add) % len(focus_table)
        new_focus_row_index = min((current_focus_row_index), len(focus_table[new_focus_col_index]) - 1)

        focus_table[current_focus_col_index][current_focus_row_index] = 0
        focus_table[new_focus_col_index][new_focus_row_index] = 1