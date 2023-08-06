import datetime
import os
import sys
import pdb
import time

import settings
import amazon_downloader
import match
import ynab_api_client
import ynab_gui_client

def equalish(a, b):
    try:
        return round(a, 4) == round(b, 4)
    except:
        return None

def get_log_name():
    return os.path.join(settings.log_path, str(settings.start_time) + '-log.txt')
log_file = open(get_log_name(), 'a+')

def log(*x, verbosity=0, sep=' | ', end=os.linesep*2):
    if verbosity >= settings.log_verbosity:
        print(datetime.datetime.now(), end=os.linesep, file=log_file)
        print(*x, sep=sep, end=end, file=log_file)
    if verbosity >= settings.print_verbosity:
        print(*x, sep=sep, end=end)


def quit():
    log('Quitting')
    if settings.close_browser_on_finish:
        driver().quit()
    log_file.close()
    sys.exit()

