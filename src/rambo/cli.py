# -*- coding: utf-8 -*-

"""Command line interface for :mod:`rambo`."""

import logging

import click

from rambo.tools import BOInitializer
from rambo.utils import init_dspy

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)


@click.command()
def hello():
    init_dspy()
    click.echo(
        "I Didn’t Come To Rescue Rambo From You. I Came Here To Rescue You From Him."
    )


@click.command()
@click.option('--prompt', default=(
    "I want to perform a Suzuki coupling with a new aryl halide, "
    "what would be the optimal conditions to start?"
), help='Provide a prompt for the synthesis suggestion.')
@click.option('--retrieval_type', default='embedding', show_default=True, 
              type=click.Choice(['embedding', 'test', 'agent'], case_sensitive=False),
              help='Specify the retrieval type.')
def suggest(prompt, retrieval_type):
    init_dspy(retrieval_type=retrieval_type)
    boinit = BOInitializer()
    resp = boinit(query=prompt)
    print(resp)


@click.group()
@click.option("--debug/--no-debug", default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


@click.group()
@click.version_option()
def main():
    """CLI for rambo."""


main.add_command(hello)
main.add_command(suggest)

if __name__ == "__main__":
    main()
