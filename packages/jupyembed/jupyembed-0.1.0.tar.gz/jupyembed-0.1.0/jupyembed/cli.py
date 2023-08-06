# -*- coding: utf-8 -*-

"""Console script for jupyembed."""
import sys
import click
from .embed import embed_data_in_notebook

@click.command()
@click.argument('notebook', type=click.Path())
@click.argument('data_files', nargs=-1, type=click.Path(exists=True))
def main(notebook, data_files):
    click.echo('Embedding data')
    embed_data_in_notebook(notebook, data_files)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
