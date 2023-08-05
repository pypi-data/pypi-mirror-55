# if --verbose, also print 200 links
# expose in beautiful cli

import re
import subprocess
import requests
import click


link_regex = r'\b(?:https?):[\w/#~:.?+=&%@!\-.:?\\-]+?(?=[.:?\-]*(?:[^\w/#~:.?+=&%@!\-.:?\-]|$))'


def url_status(url):
    try:
        return requests.head(url).status_code
    except:
        return

def all_files():
    return subprocess.check_output("git ls-files", shell=True).splitlines()


def get_links(text):
    return re.findall(link_regex, text)


def check_file(text_file, verbose=True):
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
                    click.echo(click.style("\tline " + str(line_num) + ": (" + str(status) + ")  " + link, fg="red", bold=True))          


@click.command()
@click.option('--verbose', default=False, help='If True, print valid links and redirects as well')
def run(verbose):
    files = all_files()
    click.echo(click.style("If it ain't broke, don't fix it", bold=True, fg='green'))
    click.echo(click.style("Checking " + str(len(files)) + " files in total.", bold=True))
    [check_file(f, verbose) for f in files]


if __name__ == '__main__':
    run()
