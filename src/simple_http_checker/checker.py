import requests
import logging

logger = logging.getLogger(__name__)

def check_urls(urls: list[str], timeout: int = 5) -> dict[str, str]:
    '''
    Checks a list of URLs and returns their status.

    Args: 
        urls: A list of URL strings to check. 
        timeout: Maximum time in seconds to wait for each request. Defaults to 5.

    Returns: A dictionary mapping each URL to its status string.
    '''

    logger.info(f'Checking {len(urls)} URLs with a timeout of {timeout} seconds.')
    results = {}

    for url in urls:
        status = 'Unknown'
        try:
            logger.debug(f'Checking URL: {url}')
            response = requests.get(url, timeout=timeout)
            if response.ok:
                status = f"{response.status_code} OK"
                logger.debug(f'URL {url} is OK.')
            else:
                status = f'Error: HTTP {response.status_code} {response.reason}'
                logger.warning(f'URL {url} returned HTTP {response.status_code}.')
        except requests.exceptions.Timeout:
            status = 'Error: Timeout'
            logger.warning(f'URL {url} timed out after {timeout} seconds.')
        except requests.exceptions.RequestException as e:
            status = f'Error: {str(e)}'
            logger.error(f'Error checking URL {url}: {str(e)}')
        results[url] = status
        logger.debug(f'Status for URL {url}: {status}')
    logger.info('Finished checking URLs.')
    return results