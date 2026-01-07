from rich.panel import Panel
from rich import box as rbox

def render_components(state, layout):
    layout['upper'].update(
        Panel('* 1-git-terminal-ui', title='Repo',title_align='left', **panel_style(state['focus_table'][0][0], state=state))
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
        Panel(state['input_mode'], title='Status Bar', title_align='left', **panel_style(state['focus_table'][1][1], state=state))
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

    text = ""

    all_files = []
    for type in state['git_status']:
        all_files += state['git_status'][type]

    all_files

    for type in state['git_status']:
        if len(state['git_status'][type]) > 0:
            text += type_map[type]['title']
            for file in state['git_status'][type]:
                if file['focused'] == 0:
                    text += file['file_name'][2:] + '\n'
                else:
                    text += '[black on white]' + file['file_name'][2:] + "[/black on white]" + '\n'

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
"""\
Esc: Return to navigation
"""
        )
    
    return text