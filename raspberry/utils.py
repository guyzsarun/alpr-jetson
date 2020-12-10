import os
import sys
import json
import time

from dynaconf import settings
import cv2
import requests
from datetime import datetime
import numpy as np

URL=settings.URL
TOKEN=settings.TOKEN

headers = {"Authorization": "Bearer " + TOKEN}

def line_notify(msg, payload=None, notifyDisable=False):
    if msg is None:
        msg = datetime.now()
    msg = {"message": msg, "notificationDisabled": notifyDisable}
    if payload != None:
        payload = {"imageFile": open(payload, "rb")}
    return requests.post(URL, headers=headers, params=msg, files=payload)