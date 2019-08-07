
import time

import requests

from settings import DING_TALK_URL, DOWNLOAD_DELAY, PROJECT_NAME_CN
from utils.log import logger


class Colors(object):

    WARNING = "#ec971f"
    INFO = "#449d44"
    ERROR = "#c9302c"


def send_dingding(title, text, header_text=None, color=Colors.ERROR):
    project_name = PROJECT_NAME_CN
    title = '<font color={0} >{1}</font>'.format(color, title)
    message = """## {0}\n#### {1}\n{2}\n{3}""".format(
        title, project_name, '#### {0}'.format(header_text) if header_text else '', text)
    payload = {"msgtype": "markdown",
               "markdown": {"title": title, "text": message},
               "isAtAll": True}
    try:
        requests.post(DING_TALK_URL, json=payload)
    except Exception as e:
        logger.error(e)
    time.sleep(DOWNLOAD_DELAY * 5)
