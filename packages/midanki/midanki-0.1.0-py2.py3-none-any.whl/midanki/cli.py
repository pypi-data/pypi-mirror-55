# -*- coding: utf-8 -*-

"""Console script for midanki."""
import sys
import click
import midanki


@click.command()
@click.option('--input', prompt='Choose an input',
              help='The midi input number to use.')
def main(input):
    """Console script for midanki."""
    midanki.main(int(input))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
