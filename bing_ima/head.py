# MIT License
# Copyright (c) 2024 StarWindv

import time
import os
import requests
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from concurrent.futures import ThreadPoolExecutor
import gc
from remove_dup import remove_duplicates
import argparse
import asyncio
import sys
from rename import rename_photos
