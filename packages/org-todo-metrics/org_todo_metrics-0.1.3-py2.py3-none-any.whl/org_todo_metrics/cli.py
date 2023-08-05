# -*- coding: utf-8 -*-

"""Console script for org_todo_metrics."""
import sys

import click

from .org_todo_metrics import (
    average_time_spent_working,
    debug_settings,
    mean_real_time_to_completion,
)


@click.group()
def main(args=None):
    """Console script for org_todo_metrics."""
    # click.echo(
    #     "Replace this message by putting your code into " "org_todo_metrics.cli.main"
    # )
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


@main.command()
def debug():
    debug_settings()
    return 0


@main.command()
@click.option("-f/-F", default=True)
@click.argument("org_content")
def mtc(f, org_content):
    try:
        atsw = average_time_spent_working(org_file=org_content, is_file=f)
        click.echo(f"Mean Time to Completion in seconds: {atsw}")
        return 0
    except ZeroDivisionError:
        click.echo("No completed tags found using this configuration")
        sys.exit(111)


@main.command()
@click.option("-f/-F", default=True)
@click.argument("org_content")
def mrtc(f, org_content):
    try:
        artc = mean_real_time_to_completion(org_file=org_content, is_file=f)
        click.echo(f"Mean Real Time to Completion in seconds: {artc}")
        return 0
    except ZeroDivisionError:
        click.echo("No completed tags found using this configuration")
        sys.exit(112)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
