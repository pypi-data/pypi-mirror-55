import os
import random 

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
        click.secho('\n')

def echo_prayer(prayer_name):
    with open(os.path.join(os.path.dirname(__file__), 'prayers', prayer_name)) as f:
        for l in f.readlines():
            click.secho(l, nl=False, fg='green')
        click.secho('\n')

@click.command()
@click.argument('name', default='Christ', type=click.Choice(['Christ', 'Mary', 'Trinity'], case_sensitive=False))
@click.option('--tradition', '-t', type=click.Choice(['Eastern', 'Greek', 'Catholic'], case_sensitive=False), default='Eastern', show_default=True)
@click.option('--color', '-c', is_flag=True, help='Show colored icon')
@click.option('--prayer', '-p', is_flag=True, help='Provide a short prayer')
def start(name, tradition, color, prayer):
    """This cli provides short prayers and ascii art icons
    """
    click.clear()

    color_f = 'color' if color else 'mono'

    if name.lower() in ALL_ICONS:
        echo_icon(tradition.lower(), color_f, name.lower())

    if prayer:
        prayers = os.listdir(os.path.join(os.path.dirname(__file__), 'prayers'))
        chosen_prayer = random.choice(prayers)
        echo_prayer(chosen_prayer)
    else:
        click.echo(click.style("Christ is with us", fg='green', bold=True))

if __name__ == "__main__":
    start()