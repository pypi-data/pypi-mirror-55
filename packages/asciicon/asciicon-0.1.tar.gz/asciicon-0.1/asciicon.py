import click

@click.command()
@click.argument('name', default='Christ')
def cli(name):
    """This cli provides short prayers and ascii art icons
    """
    click.echo(click.style("Christ is with us", fg='green', bold=True))

    if name.lower() == 'christ':
        with open('icons/christ.txt') as f:
            lines = f.readlines()
            
    click.clear()
    for l in lines:
        click.secho(l)
