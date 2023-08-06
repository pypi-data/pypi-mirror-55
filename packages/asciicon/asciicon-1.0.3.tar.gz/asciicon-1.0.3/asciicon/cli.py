import os
import click

ALL_ICONS = [
    'christ',
    'mary',
    'trinity'
]


def echo_icon(tradition, color_f, icon_name):
    with open(os.path.join(os.path.dirname(__file__), 'icons', tradition, color_f, f'{icon_name}.txt')) as f:
        for l in f.readlines():
            click.secho(l, nl=False)

@click.command()
@click.argument('name', default='Christ')
@click.option('--tradition', '-t', type=click.Choice(['Eastern', 'Greek', 'Catholic'], case_sensitive=False), default='Eastern', show_default=True)
@click.option('--color', '-c', is_flag=True, help='Show colored icon')
def start(name, tradition, color):
    """This cli provides short prayers and ascii art icons
    """
    click.clear()

    color_f = 'color' if color else 'mono'

    if name.lower() in ALL_ICONS:
        echo_icon(tradition.lower(), color_f, name.lower())

    click.echo(click.style("\nChrist is with us", fg='green', bold=True))

if __name__ == "__main__":
    start()