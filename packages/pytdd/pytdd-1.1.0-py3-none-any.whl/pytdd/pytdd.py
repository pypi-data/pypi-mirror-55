#!/usr/bin/env python
# -*- Mode: Python; python-indent-offset: 4 -*-
#
# Time-stamp: <2019-06-02 22:47:08 alex>
#

""" watch for file changes and start pytest (or anything else) on event
"""

import sys
import time
import logging
import configparser
import os.path
import platform
import glob
from functools import reduce

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

LOGFORMAT = '%(asctime)-15s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s'
logging.basicConfig(format=LOGFORMAT, level=logging.INFO)

__version__ = "1.1.0"
__author__ = "Alex Chauvin <ach@meta-x.org>"


def read_config():
    """read configuration file [pytdd.conf] for parameters:
       patterns=["x", "y"]
       ignore_patterns=["z"]
       cmd=["ls", "-lart"]
    """

    config_file = "pytdd.conf"

    config_params = {
        'patterns': ["*py"],
        'ignore_patterns': ["*#*", "*~"],
        'cmd': ["echo cmd unset in pytdd.conf file"],
        'force_delay': 600,
        'min_delay': 30,
    }

    if os.path.isfile(config_file):
        # Load the configuration file
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read(config_file)

        # List all contents
        section = "pytdd"
        if section in config.sections():
            for config_item in ['ignore_patterns',
                                'patterns',
                                'cmd',
                                'force_delay',
                                'min_delay']:
                try:
                    config_params[config_item] = eval(config.get(section,
                                                                 config_item))
                except configparser.NoOptionError:
                    logging.error("missing parameter in config file %s",
                                  config_item)

    return config_params


class FileChange(PatternMatchingEventHandler):
    """handle the changes of files in the directories and exec the command"""

    def __init__(self, config):
        self.cmd = config['cmd']
        self.min_delay = config['min_delay']
        super().__init__(patterns=config['patterns'],
                         ignore_patterns=config['ignore_patterns'])
        self.lastrun = 0

    def process(self, _):
        """process action on changes"""
        if time.time() - self.lastrun < self.min_delay:
            logging.info("waiting a bit")
            return

        if platform.system() == 'Windows':
            os.system("cls")
            os.system("echo %time%")
        else:
            os.system("clear ; date")

        def expand_path(x):
            if "*" in x:
                return " ".join(glob.glob(x))
            else:
                return x

        for command in self.cmd:
            print(command)
            acmd = command.split(" ")
            command = " ".join(list(map(lambda x: expand_path(x), acmd)))
            return_status = os.system(command)
            if return_status != 0:
                print("***** stopping pytdd flow")
                break

        self.lastrun = time.time()

    def on_modified(self, event):
        logging.info("file modified %s", event.src_path)
        self.process(event)

    def on_created(self, event):
        logging.info("file created %s", event.src_path)

    def on_deleted(self, event):
        logging.info("file deleted %s", event.src_path)

    def on_moved(self, event):
        logging.info("file moved %s", event.src_path)
        self.process(event)


def main():
    CONF = read_config()
    ARGS = sys.argv[1:]
    OBSERVER = Observer()
    FC = FileChange(CONF)

    print("pyTDD (v{})".format(__version__))
    print("  looking for changes on files matching: {}".format(" ".join(CONF['patterns'])))
    print("  exclude files matching: {}".format(" ".join(CONF['ignore_patterns'])))
    print("  force command each {}s".format(CONF['force_delay']))
    print("  execute command on change: {}".format(" ; ".join(CONF['cmd'])))

    OBSERVER.schedule(FC,
                      path=ARGS[0] if ARGS else '.',
                      recursive=True)
    OBSERVER.start()

    try:
        while True:
            time.sleep(CONF['force_delay'])
            FC.process(None)
    except KeyboardInterrupt:
        OBSERVER.stop()

    OBSERVER.join()


if __name__ == '__main__':
    main()
