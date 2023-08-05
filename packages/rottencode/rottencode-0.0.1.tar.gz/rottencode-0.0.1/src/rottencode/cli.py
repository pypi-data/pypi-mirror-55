import re

import click
import structlog

from . import code, events, logging, python, stats

sl = structlog.get_logger()


class Regex(click.ParamType):
    name = "regex"

    def convert(self, value, param, ctx):
        try:
            regex = re.compile(value)
            return regex
        except re.error:
            self.fail(f"`{value}` is not a valid regular expression value", param, ctx)

    def __repr__(self):
        return "REGEX"


@click.command()
@click.option("with_externals", "-e", "--ext/--no-ext", is_flag=True, default=False)
@click.option(
    "without_independent",
    "-i",
    "--no-independent/--independent",
    is_flag=True,
    default=False,
)
@click.option("cluster", "-c", "--cluster/--no-cluster", is_flag=True, default=False)
@click.option("paths", "-p", "--path", default=None, multiple=True)
@click.option("excludes", "-x", "--exclude", multiple=True, type=Regex())
def cli(with_externals, without_independent, cluster, **flags):
    logging.setup_logging(level="info")
    selection = code.Selection(**flags)
    analysis = stats.ModuleAnalysis(
        selection,
        with_externals=with_externals,
        without_independent=without_independent,
        cluster=cluster,
    )
    analysis.report()


def main():
    cli()
