import subprocess
import os

from render import get_git_status_focused_file

cwd = r"C:\Users\jeanb\Documents\misc-code\fake-folder-to-test-git"

def get_repo_name(state):
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        cwd=cwd
    )

    if result.returncode == 0:
        state["repo_name"] = os.path.basename(result.stdout.strip())


def get_git_status(state):
    result = subprocess.run(
        ['git', 'status', '--porcelain', '-u'],
        capture_output=True,
        text=True,
        cwd=cwd
        )
    
    if not result.returncode:

        state['git_status'] = []

        files = result.stdout.split('\n')

        for file in files:
            if file.startswith('A') or file.startswith('M'):
                state['git_status'].append({"file_name": file, 'type': "to_be_commited", "focused": False})
            if file.startswith(' '):
                state['git_status'].append({"file_name": file, 'type': "not_staged_for_commit", "focused": False})
            if file.startswith('??'):
                state['git_status'].append({"file_name": file, 'type': "untracked", "focused": False})
    

def get_git_branch(state):
    result = subprocess.run(
        ["git", 'branch'],
        capture_output=True,
        text=True,
        cwd=cwd
    )

    if not result.returncode:
        state['git_branch'] = result.stdout

def get_git_log(state):
    result = subprocess.run(
        ['git', 'log', '--oneline'],
        capture_output=True,
        text=True,
        cwd=cwd
    )

    if not result.returncode:
        state['git_log'] = result.stdout
    

def call_and_parse_git(state):
    get_repo_name(state=state)
    if not ((state['input_mode'] == 'focused') and (state['focus_table'][1][0])):
        get_git_status(state)
    get_git_branch(state)
    get_git_log(state)



def git_add_file(state):
    focused_file = get_git_status_focused_file(state=state)
    result = subprocess.run(
        ['git', 'add', focused_file['file_name'][3:], '-v'],
        capture_output=True, 
        text=True,
        cwd=cwd,
    )

    if not result.returncode:
        state['debug'] = result.stdout

    return not result.returncode

def git_restore_file(state):
    focused_file = get_git_status_focused_file(state=state)
    result = subprocess.run(
        ['git', 'restore', '--staged', focused_file['file_name'][3:]],
        capture_output=True, 
        text=True,
        cwd=cwd,
    )

    state['debug'] = result.returncode
    if not result.returncode:
        state['debug'] = result.stdout

    return not result.returncode



if __name__ == "__main__":
    print(get_git_status({}))