import msvcrt

from git import git_add_file, get_git_status, git_restore_file, git_commit

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
            if state['focus_table'][1][0]:
                state['git_status'][0]['focused'] = True
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
            if key == b'\xe0':
                key = msvcrt.getch()
                if key == b'H':
                    state['direction'] = "up"
                    update_git_status_focus(state)
                elif key == b'P':
                    state['direction'] = "down"
                    update_git_status_focus(state)

            elif (key == b'a') or (key == b'A'):
                git_add_file(state=state)
                get_git_status(state=state)
                if len(state['git_status']) > 0:
                    state['git_status'][0]["focused"] = 1
            elif (key == b'r') or (key == b'R'):
                git_restore_file(state=state)
                get_git_status(state=state)
                if len(state['git_status']) > 0:
                    state['git_status'][0]["focused"] = 1
            elif (key == b'c') or (key == b'C'):
                state['input_mode'] = "typing_navigation"     
        
        elif state['focus_table'][1][1]:
            pass

    elif state['input_mode'] == "typing_navigation":
        if key == b'\x1b':
            state['debug'] = "Typing enabled"
            state['input_mode'] = "navigation"
        elif key == b'\r':
            state['input_mode'] = "typing"
        elif key == b'\t':
            state['typing_mode_focus_title'] = not state['typing_mode_focus_title']
        elif (key == b'c') or (key == b'C'):
            worked = git_commit(state)
            if worked:
                state['input_mode'] = 'navigation'
                state['typing_mode_focus_title'] = True
                state['typed_commit_title'] = ""
                state['typed_commit_description'] = ""




        elif key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H':
                state['direction'] = "up"
                state['typing_mode_focus_title'] = not state['typing_mode_focus_title']
            elif key == b'P':
                state['direction'] = "down"
                state['typing_mode_focus_title'] = not state['typing_mode_focus_title']

    elif state['input_mode'] == "typing":
        if key == b'\x1b':
            state['debug'] = "Typing enabled"
            state['input_mode'] = "typing_navigation"
        elif key == b'\xe0':
            key = msvcrt.getch()
            pass
        elif (key == b'\r') and (not state['typing_mode_focus_title']):
            state['typed_commit_description'] += '\n'
        elif key == b'\x08':
            if state['typing_mode_focus_title']:
                state['typed_commit_title'] = state['typed_commit_title'][:-1]
            else:
                state['typed_commit_description'] = state['typed_commit_description'][:-1]
        else: 
            typed_letter = key.decode('cp850')
            if state['typing_mode_focus_title']:
                state['typed_commit_title'] = state['typed_commit_title'] + typed_letter
            else:
                state['typed_commit_description'] = state['typed_commit_description'] + typed_letter





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

def update_git_status_focus(state):
    
    for index, file in enumerate(state['git_status']):
        if file['focused'] == 1:
            break

    if state['direction'] == 'up':
        to_add = -1
    elif state['direction'] == "down":
        to_add = 1
    else: 
        to_add = 0

    state['git_status'][index]['focused'] = 0
    state['git_status'][(index+to_add) % len(state['git_status'])]['focused'] = 1

    

