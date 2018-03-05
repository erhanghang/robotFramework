# -*- coding: utf-8 -*-
# Create by PGQ
#安装环境PIL，tesseract-ocr，pytesseract

__version__ = '0.1'

from robot.api import logger
import Image,ImageEnhance
import ConfigParser, os
import pytesseract
import cStringIO
import urllib2


Default = ""
filename = "pgq_para.ini"
cfg = ConfigParser.ConfigParser()


def iniGetValue(Section, Key):
    readhandle = open(filename)
    cfg.readfp(readhandle)
    try:
        value = cfg.get(Section, Key)
        readhandle.close()
    except:
        value = Default
    return value


def iniSetValue(Section, Key, Value):
    writehandle = open(filename, 'w')
    try:
        cfg.set(Section, Key, Value)
    except:
        cfg.add_section(Section)
        cfg.set(Section, Key, Value)
        cfg.write(writehandle)
    writehandle.close()


if __name__ == '__main__':
    # print iniGetValue("GLOBE", "username")
    # f.iniSetValue("hh","h1","h11")
    print "test"
