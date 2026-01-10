from rich.layout import Layout
from rich.text import Text

def make_layout():
    layout = Layout()

    layout.split_column(
        Layout(name='app'),
        Layout(name='keybinds', size=1),
        
    )

    layout['app'].split_row(
        Layout(name="left", ratio=3),
        Layout(name="right", ratio=7)
    )
    layout['app']['left'].split_column(
        Layout(name='upper', size=3),
        Layout(name='middle', ratio = 3),
        Layout(name='lower', ratio = 7),
    )
    layout['app']['right'].split_column(
        Layout(name='main'),
        Layout(name='footer', size=3)
    )

    return layout

def make_typing_layout():
    typing_layout = Layout()

    typing_layout.split_column(
        Layout(renderable=Text(' '), name="temp1", ratio = 2),
        Layout(name="center", ratio=6),
        Layout(renderable=Text(' '), name='temp2', ratio =2),
        Layout(name='keybinds', size =1)

    )

    typing_layout['center'].split_row(
        Layout(renderable=Text(' '), name="temp3", ratio = 2),
        Layout(name="input_box", ratio=6),
        Layout(renderable=Text(' '), name='temp4', ratio =2)
    )

    typing_layout['input_box'].split_column(
        Layout(name = "input_title", size = 3),
        Layout(name = "input_description")
    )

    return typing_layout