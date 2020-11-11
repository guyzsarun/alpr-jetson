import os
import sys

from dynaconf import settings
import requests
from datetime import datetime
import time


URL=settings.URL
TOKEN=settings.TOKEN

def line_notify(msg, payload=None, notifyDisable=False):
    headers = {"Authorization": "Bearer " + TOKEN}
    if msg is None:
        msg = datetime.now()
    msg = {"message": msg, "notificationDisabled": notifyDisable}
    if payload != None:
        payload = {"imageFile": open(payload, "rb")}
    return requests.post(URL, headers=headers, params=msg, files=payload)
