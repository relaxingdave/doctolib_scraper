import logging

import bs4 as bs
import requests

logging.basicConfig(
    level=logging.INFO
)
logger = logging.getLogger()


def get_dict_from_url(url, proxy):

    if proxy:
        ip, port = get_proxy_server()

        logger.info(f'Use proxy server {ip} to query {url}...')

        # some proxies only allow for http requests
        proxy = {
            "http": f"http://{ip}:{port}",
        }

        url_dict = (
            requests
            .get(
                url,
                headers={'User-Agent': 'Mozilla/5.0'},
                proxies=proxy,
            )
            .json()
        )

    else:
        url_dict = (
            requests
            .get(url, headers={'User-Agent': 'Mozilla/5.0'})
            .json()
        )

    return url_dict


def get_proxy_server():
    """
    Get the first proxy server ip and port listed on
    `https://free-proxy-list.net`
    """
    r = requests.get("https://free-proxy-list.net/")
    soup = bs.BeautifulSoup(r.text, "html.parser")
    table_body = soup.find('table').find('tbody')

    # get the first proxy server
    row = table_body.find('tr')
    ip = row.find_all('td')[0].text
    port = row.find_all('td')[1].text

    return ip, port
