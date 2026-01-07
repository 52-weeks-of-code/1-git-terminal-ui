import subprocess

def get_git_status(state):
    result = subprocess.run(
        ['git', 'status', '--porcelain', '-u'],
        capture_output=True,
        text=True,
        )
    
    if not result.returncode:

        state['git_status'] = {
            "to_be_commited": [],
            "not_staged_for_commit": [],
            "untracked": [],
        }

        files = result.stdout.split('\n')

        for file in files:
            if file.startswith('A'):
                state['git_status']['to_be_commited'].append({"file_name": file, "focused": False})
            if file.startswith(' M'):
                state['git_status']['not_staged_for_commit'].append({"file_name": file, "focused": False})
            if file.startswith('??'):
                state['git_status']['untracked'].append({"file_name": file, "focused": False})
    

def get_git_branch(state):
    result = subprocess.run(
        ["git", 'branch'],
        capture_output=True,
        text=True,
    )

    if not result.returncode:
        state['git_branch'] = result.stdout

def get_git_log(state):
    result = subprocess.run(
        ['git', 'log', '--oneline'],
        capture_output=True,
        text=True
    )

    if not result.returncode:
        state['git_log'] = result.stdout
    

def call_and_parse_git(state):
    get_git_status(state)
    get_git_branch(state)
    get_git_log(state)



if __name__ == "__main__":
    print(get_git_status({}))