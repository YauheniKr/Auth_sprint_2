import logging
from time import sleep
import requests
import http


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

URL = 'http://nginx/apidocs/'


def make_request():
    status = requests.head(URL)
    return status


def check_api_availability():
    while True:
        try:
            make_request()
            if make_request().status_code == http.HTTPStatus.OK:
                logger.info("API server running")
                exit(0)
            else:
                logger.error("API is not available. Sleep for 10 sec")
                sleep(10)
        except requests.exceptions.ConnectionError:
            logger.error("API is not available. Sleep for 10 sec")
            sleep(10)
        else:
            exit(1)


if __name__ == '__main__':
    check_api_availability()
