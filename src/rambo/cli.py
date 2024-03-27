# -*- coding: utf-8 -*-

"""Command line interface for :mod:`rambo`.

Why does this file exist, and why not put this in ``__main__``? You might be tempted to import things from ``__main__``
later, but that will cause problems--the code will get executed twice:

- When you run ``python3 -m rambo`` python will execute``__main__.py`` as a script.
  That means there won't be any ``rambo.__main__`` in ``sys.modules``.
- When you import __main__ it will get executed again (as a module) because
  there's no ``rambo.__main__`` in ``sys.modules``.

.. seealso:: https://click.palletsprojects.com/en/8.1.x/setuptools/#setuptools-integration
"""

import logging

import click
from rambo.utils import init_dspy
from rambo.rag import BOInitializer

__all__ = [
    "main",
]

logger = logging.getLogger(__name__)

@click.command()
def hello():
    init_dspy()
    click.echo("I Didn’t Come To Rescue Rambo From You. I Came Here To Rescue You From Him.")

@click.command()
def suggest_me_a_synthesis(query: str ="i'm running a suzuki coupling reaction. what are the initial conditions?"):
    init_dspy()
    
    click.echo("Suggesting a synthesis...")
    # format natural language prompt into input for RAG
    # retrieve k relevant passages (ReAct with RAG as tool)
    # convert retrieval output into useable output
    # call BO
    # evaluate
    boinit = BOInitializer()
    resp = boinit(query=query)
    print(resp)
    

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(f"Debug mode is {'on' if debug else 'off'}")

@cli.command()
def main():
    """CLI for rambo."""

main.add_command(hello)

if __name__ == "__main__":
    main()
