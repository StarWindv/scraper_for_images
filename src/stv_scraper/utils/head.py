# MIT License
# Copyright (c) 2024 星灿长风v(StarWindv)

import time
import os
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
import gc
import argparse
import asyncio
import sys
import threading
from PIL import Image
import imagehash
import io