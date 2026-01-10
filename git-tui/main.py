from rich.console import Console, Group
from rich.layout import Layout
from rich.panel import Panel
from rich.tree import Tree
from rich.text import Text
from rich import box
from rich.live import Live
import msvcrt
from time import sleep

from layout import make_layout, make_typing_layout
from state import create_state
from render import render_components
from input import manage_input
from git import call_and_parse_git

console = Console()
layout = make_layout()
typing_layout = make_typing_layout()

state = create_state(layout)

### Render
with Live(renderable=Text(" "), console = console, refresh_per_second=24, screen=True, transient=True) as live:

    live.update(Text(" "))
    call_and_parse_git(state=state)
    render_components(
        state=state, 
        layout=layout, 
        typing_layout=typing_layout, 
        live = live,
        console = console,
        )
    
    live.update(layout)

    while True:
        call_and_parse_git(state=state)
        if msvcrt.kbhit():
            key = msvcrt.getch()
            print(key)
            manage_input(key, state=state)

        render_components(
            state=state, 
            layout=layout, 
            typing_layout=typing_layout, 
            live = live,
            console = console,
            )

                





print(console.size)
