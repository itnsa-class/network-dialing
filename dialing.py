#!/usr/bin/env python3
# coding: utf-8
# version: 0.0.1
# author: Anonymous


from urllib.request import urlopen, Request
from urllib.parse import urlencode
from argparse import ArgumentParser

import json
import sys
import time
import os


SLEEP_TIME = 14 * 60

def custom_parmeter(username, passwd):
    req_address = "http://192.168.99.5/PortalServer/customize_new/1604888504954/phone/auth.jsp?isPasscode=N&browserFlag=zh&folderName=1604888504954/phone&httpsFlag=N&publicBarcodeEncode=null&authSuccess=3&redirectUrl=&urlParameter=&currentTime=1610612871472"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    # refrer = "http://192.168.99.5:8080/PortalServer/customize_new/1541223647104/pc/auth.jsp"
    origin = "http://192.168.99.5:8080"
    data = {
      #  "userName": username,
      #  "password": passwd,
        "userName": "account",
        "password": "password",
        "hasValidateCode": False,
        "autoLogin": False
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": origin,
        # "Referer": refrer,
        "User-Agent": user_agent
    }
    return req_address, data, header



def login(addr, data, header):
    req = Request(addr, urlencode(data).encode("utf8"), header)
    resp = urlopen(req)
    return resp

def daemon(callback, argc):
    global SLEEP_TIME
    try:
        while True:
            u, d, h = argc
            callback(u, d, h)
            time.sleep(SLEEP_TIME)
    except KeyboardInterrupt:
        sys.stdout.writelines("exit...")
        



def main():
    username = "account"
    passwd = "password"

    parser = ArgumentParser()
    parser.add_argument("--daemon", "-d", action="store_true", help="open daemon login..")
    parser.add_argument("--one", "-o", action="store_true", help="log in once.")
    parser.add_argument("--username", "-u", help="(options) login user name.")
    parser.add_argument("--password", "-p", help="(options) login password")
    argv = parser.parse_args()
    if argv.username:
        username = argv.username
    if argv.password:
        passwd = argv.password
    if argv.daemon:
        argc = custom_parmeter(username, passwd)
        daemon(login, argc)
    elif argv.one:
        u, d, h = custom_parmeter(username, passwd)
        login(u, d, h)
    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
