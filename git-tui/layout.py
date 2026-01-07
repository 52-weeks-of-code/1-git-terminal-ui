from rich.layout import Layout


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