# -*- coding: utf-8 -*-

"""Console script for loganalyzer."""
import sys
import click

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
@click.option('--foo/--no-foo', default=False)
@click.option('-f', '--filename', 'filename', default='logging.yaml')
def main(foo, filename):
    """Console script for loganalyzer."""
    click.echo("Hello {} : {}".format(foo, filename))
    return 0



if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
