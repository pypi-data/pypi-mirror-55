import click
from dots.checker import SystemChecker
from dots.config import DEFAULT_SOURCE_DIR, HOME_DIR
from dots.repository import Repository
from dots.utils import task


@click.group()
@click.option(
    "--src-dir",
    type=click.Path(),
    default=DEFAULT_SOURCE_DIR,
    help="Location to use as dotfiles directory",
)
@click.option(
    "--dest-dir",
    type=click.Path(exists=True),
    default=HOME_DIR,
    help="Location to create symlinks",
)
@click.option(
    "-n",
    "--dry-run",
    default=False,
    is_flag=True,
    help="Enable debugging mode (implies --verbose)",
)
@click.option(
    "--depth",
    default=3,
    type=int,
    help='How deep to recurse looking for ".symlink" items',
)
@click.option(
    "-v",
    "--verbose",
    default=False,
    is_flag=True,
    help="Show what commands have been executed.",
)
@click.pass_context
def cli(ctx, src_dir, dest_dir, dry_run, depth, verbose):
    if dry_run:
        verbose = True

    ctx.obj["repository"] = Repository(src_dir, dest_dir, depth, verbose, dry_run)


@cli.command()
@click.argument("topics", nargs=-1)
@click.pass_context
def sync(ctx, topics):
    """Update the symlinks
    """
    with task("Syncing dotfiles"):
        ctx.obj["repository"].sync(topics)


@cli.command()
@click.pass_context
def clean(ctx):
    """Removes stale/broken symlinks
    """
    with task("Cleaning broken symlinks"):
        ctx.obj["repository"].clean()


@cli.command()
@click.pass_context
def check(ctx):
    """Check whether a system is setup correctly.
    """
    checker = SystemChecker()
    checker.run(ctx.obj["repository"].source_dir + "/tools/checks.yaml")


def main():
    cli(obj={}, auto_envvar_prefix="DOTFILES")
