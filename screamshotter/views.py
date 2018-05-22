#!/usr/bin/env python3

from optparse import OptionParser

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from django.shortcuts import HttpResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_PATH = '/usr/bin/chromium-browser'
CHROMEDRIVER_PATH = '/usr/lib/chromium-browser/chromedriver'
WINDOW_SIZE = "1920,1080"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

schemes = (
    'http',
    'https',
)


def make_screenshot(url, waitfor=None, output=None):
    if not url.startswith(schemes):
        raise Exception('URLs need to start with "{}"'.format(' or '.join(schemes)))

    driver = webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH,
        chrome_options=chrome_options
    )
    driver.get(url)

    if waitfor:
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, waitfor))
            )
            print(element)
        finally:
            driver.quit()

    # if save screenshot
    data = driver.get_screenshot_as_png()
    driver.close()
    return data


def view(request):
    data = make_screenshot(url=request.GET['url'], waitfor=request.GET.get('waitfor', None))
    response = HttpResponse(data, content_type='image/png')
    #response['Content-Disposition'] = 'file; attachment;'
    return response
