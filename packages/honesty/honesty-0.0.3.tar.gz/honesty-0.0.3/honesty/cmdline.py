import sys

import click
import pkg_resources

from honesty.checker import has_nativemodules, is_pep517, run_checker
from honesty.releases import parse_index


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.argument("package_name")
def list(package_name: str) -> None:
    package = parse_index(package_name)
    print(f"package {package.name}")
    print("releases:")
    for k, v in package.releases.items():
        print(f"  {k}:")
        for f in v.files:
            print(f"    {f.basename}")


@cli.command()
@click.option("--verbose", "-v", is_flag=True, type=bool)
@click.option("--fresh", "-f", is_flag=True, type=bool)
@click.argument("package_name")
@click.argument("version", default="latest")
def check(verbose: bool, fresh: bool, package_name: str, version: str) -> None:
    package = parse_index(package_name, fresh=fresh)
    if version == "latest":
        if not package.releases:
            raise click.ClickException("No releases at all")
        version = sorted(package.releases, key=pkg_resources.parse_version)[-1]

    if verbose:
        click.echo(f"check {package_name} {version}")

    rc = 0
    if version == "*":
        for v in sorted(package.releases, key=pkg_resources.parse_version):
            rc |= run_checker(package, v, verbose=verbose)
    else:
        rc |= run_checker(package, version, verbose=verbose)

    if rc != 0:
        sys.exit(rc)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, type=bool)
@click.option("--fresh", "-f", is_flag=True, type=bool)
@click.argument("package_name")
@click.argument("version", default="latest")
def ispep517(verbose: bool, fresh: bool, package_name: str, version: str) -> None:
    package = parse_index(package_name, fresh=fresh)
    if version == "latest":
        if not package.releases:
            raise click.ClickException("No releases at all")
        version = sorted(package.releases, key=pkg_resources.parse_version)[-1]

    if verbose:
        click.echo(f"check {package_name} {version}")

    if not is_pep517(package, version, verbose=verbose):
        sys.exit(1)


@cli.command()
@click.option("--verbose", "-v", is_flag=True, type=bool)
@click.option("--fresh", "-f", is_flag=True, type=bool)
@click.argument("package_name")
@click.argument("version", default="latest")
def native(verbose: bool, fresh: bool, package_name: str, version: str) -> None:
    package = parse_index(package_name, fresh=fresh)
    if version == "latest":
        if not package.releases:
            raise click.ClickException("No releases at all")
        version = sorted(package.releases, key=pkg_resources.parse_version)[-1]

    if verbose:
        click.echo(f"check {package_name} {version}")

    if has_nativemodules(package, version, verbose=verbose):
        sys.exit(1)


if __name__ == "__main__":
    cli()
