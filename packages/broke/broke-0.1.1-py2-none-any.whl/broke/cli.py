#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import subprocess
import requests
import click

# This is already monstrous, but certainly doesn't catch "all" cases
LINK_REGEX = r'\b(?:https?):[\w/#~:.?+=&%@!\-.:?\\-]+?(?=[.:?\-]*(?:[^\w/#~:.?+=&%@!\-.:?\-]|$))'


def url_status(url):
    """Get URL status through a HEAD request. Avoid unlimited retries."""
    try:
        return requests.head(url).status_code
    except:
        return


def all_git_files():
    """Return all files tracked by git, excluding those
    in .gitignore to avoid clutter.
    """
    lines = subprocess.check_output("git ls-files", shell=True).splitlines()
    return [l.decode() for l in lines]


def get_links(text):
    """Find all links in a piece of text."""
    return re.findall(LINK_REGEX, text)


def check_file(text_file, verbose=True):
    """Check a file for links and echo the file, links
    and HTTP status codes on the command line.
    """
    printed_file = False
    with open(text_file, 'r') as text:
        for line_num, line in enumerate(text):
            links = get_links(line)
            for link in links:
                status = url_status(link)
                if status and (status >= 400 or verbose):
                    if not printed_file:
                        click.echo(click.style("File: " + text_file, bold=True))
                        printed_file = True
                    click.echo(click.style("\tline " + str(line_num) +
                                           ": (" + str(status) + ")  " + link, fg="red", bold=True))


@click.command()
@click.option('--verbose', default=False, help='If True, print valid links and redirects as well')
def run(verbose):
    """Main entry-point for broke.
    """
    files = all_git_files()
    click.echo(click.style(
        "If it ain't broke, don't fix it", bold=True, fg='green'))
    click.echo(click.style("Checking " + str(len(files)) +
                           " files in total.", bold=True))
    [check_file(f, verbose) for f in files]


if __name__ == '__main__':
    run()
