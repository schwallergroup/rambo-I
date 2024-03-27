# -*- coding: utf-8 -*-

"""Command line interface for :mod:`rambo`."""

import logging

import click
from rambo.utils import init_dspy
from rambo.tools import BOInitializer

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)

@click.command()
def hello():
    click.echo("I Didn’t Come To Rescue Rambo From You. I Came Here To Rescue You From Him.")

@click.command()
def suggest_me_a_synthesis(
    prompt: str = '''
    I want to perform a Suzuki coupling with a new aryl halide, namely ... .
    I have the following ligands available
    what are the initial conditions?
    '''
):
    init_dspy()
    boinit = BOInitializer()
    resp = boinit(query=prompt)
    print(resp)
    
@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

main.add_command(hello)
main.add_command(suggest_me_a_synthesis)

if __name__ == "__main__":
    main()
