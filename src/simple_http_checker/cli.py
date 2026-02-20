import logging
import click
from .checker import check_urls

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)-8s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@click.command()
@click.argument("urls", nargs=-1)
@click.option(
    "--timeout",
    default=5,
    help="Maximum time in seconds to wait for each request. Defaults to 5.",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="If set, enables debug logging for more detailed output.",
)
def main(urls, timeout, verbose):
    """
    A simple HTTP checker that checks the status of provided URLs.

    Args:
        urls: A comma-separated list of URLs to check.
        timeout: Maximum time in seconds to wait for each request. Defaults to 5.
        verbose: If set, enables debug logging for more detailed output.
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled. Debug logging is active.")

    if not urls:
        logger.error("No URLs provided. Please provide at least one URL to check.")
        return

    logger.debug(f"Raw input URLs: {urls}")
    logger.debug(f"Timeout value: {timeout} seconds")

    url_list = [url.strip() for url in urls]
    logger.info(f"Checking {len(url_list)} URLs with a timeout of {timeout} seconds.")

    results = check_urls(url_list, timeout)

    click.echo("\nResults:")
    for url, status in results.items():
        if "OK" in status:
            fg_color = "green"
        else:
            fg_color = "red"
        click.echo(click.style(f"{url}: {status}", fg=fg_color))
