from rich.panel import Panel
from rich import box as rbox
from rich.text import Text

import math

def render_components(state, layout, typing_layout, live, console):
    if (state['input_mode'] == "navigation") or (state['input_mode'] == "focused"):
        live.update(
            layout
        )

        left_side_width = math.floor(layout['left'].ratio * console.size[0] / 10)
        right_side_width = math.floor(layout['right'].ratio * console.size[0] / 10)

        layout['upper'].update(
            Panel(
                renderable=git_repo_name_clean(state, width=left_side_width), 
                title='Repo',
                title_align='left', 
                **panel_style(state['focus_table'][0][0], state=state)
                )
        )

        layout['middle'].update(
            Panel(
                renderable=git_branch_clean(state, left_side_width),
                title='Branches', 
                title_align='left', 
                **panel_style(state['focus_table'][0][1], state=state)
                ),
            )

        layout['lower'].update(
            Panel(
                renderable=git_log_clean(state, left_side_width),
                title='Commit log', 
                title_align='left', 
                **panel_style(state['focus_table'][0][2], state=state)
                )
        )

        layout['main'].update(
            Panel(
                renderable=git_status_clean(state), 
                title='Git Status', 
                title_align='left', 
                **panel_style(state['focus_table'][1][0], state=state)
                )
        )

        layout['footer'].update(
            Panel(
                renderable=state['debug'], 
                title='Debug', 
                title_align='left', 
                **panel_style(state['focus_table'][1][1], state=state)
                )
        )

        layout['keybinds'].update(
            renderable=keybinds_renderable(state)
        )
    
    elif (state['input_mode'] == "typing_navigation") or (state['input_mode'] == "typing"):
        live.update(
            typing_layout
        )

        typing_layout['input_title'].update(
            Panel(
                renderable=Text(state['typed_commit_title']),
                title="Commit Title",
                title_align='left',
                **typing_panel_style(state, state['typing_mode_focus_title']),
                )
        )

        typing_layout['input_description'].update(
            Panel(
                renderable=Text(state['typed_commit_description']),
                title="Describe your commit",
                title_align="left",
                **typing_panel_style(state, not state['typing_mode_focus_title']),
                )
        )

        typing_layout['keybinds'].update(
            keybinds_renderable(state)
        )



def panel_style(corresponding_panel, state):
    border_style = []
    box = rbox.SQUARE

    if corresponding_panel == 1:
        border_style.append("cyan")

        if state['input_mode'] == 'focused':
            box = rbox.DOUBLE
            border_style.append('cyan')


    
    return {
        "box": box,
        "border_style" : ' '.join(border_style),
        }

def typing_panel_style(state, corresponding_boolean):
    border_style = []
    box = rbox.SQUARE

    if corresponding_boolean:
        border_style.append("cyan")

        if state['input_mode'] == 'typing':
            box = rbox.DOUBLE
            border_style.append('cyan')

    return {
        "box": box,
        "border_style" : ' '.join(border_style),
        }

def git_repo_name_clean(state, width):
    repo_name = state['repo_name']

    if len(repo_name) > (width - 5):
        repo_name = repo_name[:width-7]
        repo_name = repo_name + '...'

    return repo_name



def git_status_clean(state):

    type_map = {
        "to_be_commited": {
            "title" : "[bold green]Changes to be commited:[/bold green] \n"
        },
        "not_staged_for_commit" : {
            "title" : "[bold yellow]Changes not staged for commit:[/bold yellow] \n"
        },
        "untracked" : {
            "title" : "[bold red]Untracked files:[/bold red] \n"
        },
    }

    types_seen = []
    for file in state['git_status']:
        types_seen.append(file['type'])
    types_seen = list(set(types_seen))


    text = ""
    if len(state['git_status']) > 0:
        for i, file in enumerate(state['git_status']):
            if (file['type'] in type_map.keys()) and (file['type'] in types_seen):
                text += type_map[file['type']]['title']
                types_seen = [git_type for git_type in types_seen if git_type != file['type']]

            if file['focused'] == 0:
                text += "| " + file['file_name'][3:] + '\n'
            else:
                text += "> [black on white]" + file['file_name'][3:] + '\n[/black on white]'

    return text


def git_log_clean(state, width):
    git_log_list = state['git_log'].split('\n')

    commit_code_style = 'bold yellow'

    output = ""
    for git_log_line in git_log_list[:-1]:
        code = git_log_line.split(' ')[0]
        description = ' '.join(git_log_line.split(' ')[1:])

        pretty_log = f"[{commit_code_style}]{code}[/{commit_code_style}] {description}"
        if (len(pretty_log) - len(commit_code_style)*2 + 5) > (width + 2):
            pretty_log = pretty_log[:len(commit_code_style)*2 + 5 + int(width - 7)]
            pretty_log += "..."

        output += pretty_log + "\n"

    return output

def git_branch_clean(state, width):
    git_branch = state['git_branch'].split('\n')


    git_branch_line_style = "bold yellow"
    output = ""
    for git_branch_line in  git_branch:
        pretty_git_branch_line = git_branch_line
        if len(pretty_git_branch_line) > (width - 7):
            pretty_git_branch_line = pretty_git_branch_line[:int(width - 7)]
            pretty_git_branch_line =  pretty_git_branch_line + "..."

        if git_branch_line.startswith('*'):
            output += f'[{git_branch_line_style}]' + pretty_git_branch_line + f'[/{git_branch_line_style}]' + "\n"
        else:
            output += git_branch_line + '\n'

    return output




    
def keybinds_renderable(state):
    text = ""
    if state['input_mode'] == "navigation":
        text += (
""" \
Arrow Keys: Navigate between windows    \
Enter: Focus on a view
""")
    elif state['input_mode'] == "focused":
        text += (
""" \
Esc: Return to navigation    \
"""
        )
        if state['focus_table'][1][0]:
            focused_file = get_git_status_focused_file(state)
            if focused_file:
                text += (
"""\
C: Commit changes    \
"""
                )
            
                

                if focused_file['type'] == "not_staged_for_commit":
                    text += (
"""\
A: Add file to be commited    \
R: Discard changes    \
""")
                elif focused_file['type'] == "to_be_commited":
                    text += (
"""\
R: Unstage    \
""")
                elif focused_file['type'] == "untracked":
                    text += (
"""\
A: Add file to be commited    \
""")
                else:
                    text += "Arrow Keys: Navigate between files"
    
    elif state['input_mode'] == "typing_navigation":
        text += (
""" \
Esc: Cancel    \
Tab/Up/Down: Navigate    \
Enter: Start Typing    \
C: Commit
""")
        
    elif state['input_mode'] == "typing":
        text += (
""" \
Esc: Cancel    \
Letters: Type
""")

    return text

def get_git_status_focused_file(state):
    for file in state['git_status']:
        if file['focused']:
            return file