from rich.panel import Panel
from rich import box as rbox

def render_components(state, layout):
    layout['upper'].update(
        Panel(f'* {state['repo_name']}', title='Repo',title_align='left', **panel_style(state['focus_table'][0][0], state=state))
    )

    layout['middle'].update(
        Panel(state['git_branch'], title='Branches', title_align='left', **panel_style(state['focus_table'][0][1], state=state)),
        )

    layout['lower'].update(
        Panel(
            state['git_log'] ,title='Commit log', title_align='left', **panel_style(state['focus_table'][0][2], state=state))
    )

    layout['main'].update(
        Panel(git_status_clean(state), title='Git Status', title_align='left', **panel_style(state['focus_table'][1][0], state=state))
    )
    layout['footer'].update(
        Panel(state['debug'], title='Status Bar', title_align='left', **panel_style(state['focus_table'][1][1], state=state))
    )

    layout['keybinds'].update(
        keybinds_renderable(state)
    )


def panel_style(corresponding_panel, state):
    border_style = []
    box = rbox.SQUARE

    if corresponding_panel == 1:
        border_style.append("yellow")

        if state['input_mode'] == 'focused':
            box = rbox.DOUBLE
            border_style.append('yellow')


    
    return {
        "box": box,
        "border_style" : ' '.join(border_style),
        }

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
C: Commit changes    \
"""
        )
        if state['focus_table'][1][0]:
            focused_file = get_git_status_focused_file(state)
            if focused_file:
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
    
    return text

def get_git_status_focused_file(state):
    for file in state['git_status']:
        if file['focused']:
            return file