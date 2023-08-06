import click
from viptela.vmanage.cli.show.device import device
from viptela.vmanage.cli.show.template import template
from viptela.vmanage.cli.show.policy import policy
from viptela.vmanage.cli.show.omp import omp
from viptela.vmanage.cli.show.control import control

@click.group()
@click.pass_context
def show(ctx):
    """
    Show commands
    """

show.add_command(device)
show.add_command(template)
show.add_command(policy)
show.add_command(omp)
show.add_command(control)