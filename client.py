#!/usr/bin/python
import signal
import time
import os
from selenium import webdriver

def test_request(arg=None):
    """Your http request."""
    time.sleep(2)
    return arg

class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()

# performing login action
def site_login():
    
    # initialize chrome browser
    driver = webdriver.Chrome()
    
    # go the ther website that vulnerable to XSS and perfrom certain action
    driver.get("http://35.231.36.102:1779/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("verysecuredpassword")
    driver.find_element_by_name("submit").click()
    
    # accept any alert that popped up
    while True:
        try:
            alert = driver.switch_to_alert()
            alert.accept()
            time.sleep(0.5)
        except:
            break

    # maintaing the session for 2 minutes
    time.sleep(120)
    
    # click logout
    driver.get("http://35.231.36.102:1779/logout.php")
    
    # close browser
    driver.quit()

i = 0
while True:
    try:
        # timer
        with Timeout(180):
            site_login()
            print i, "Logged in."
    # force close the browser after some time.
    except Timeout.Timeout:
        pass
        os.system("pkill chromium-browser")
        print i, "Timeout"
    except:
        pass
        os.system("pkill chromium-browser")
        print i, "Failed for some reason"

    i += 1
