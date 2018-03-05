# -*- coding: utf-8 -*-
# Create by PGQ
#安装环境PIL，tesseract-ocr，pytesseract

__version__ = '0.1'

from robot.api import logger
from PIL import Image
from PIL import ImageEnhance
import pytesseract
import cStringIO, StringIO
import urllib2
import ConfigParser, os
import random
from datetime import date
from datetime import timedelta
import mysqlDBUtil
import Tkinter
import tkMessageBox
import tkSimpleDialog




Default = ""
filename = "pgq_para.ini"
cfg = ConfigParser.ConfigParser()


def getTishi(prompt):
    u'''弹出提示对话框，获取输入的内容
        | ${tmp}                  | getTishi                 |请输入验证码：
       '''
    top = Tkinter.Tk()
    top.withdraw()
    try1 = tkSimpleDialog.askstring('提示：      ', prompt)
    return try1

def setTishi(prompt):
    u'''弹出提示对话框，设置提示的内容
        | setTishi               |请输入验证码：
       '''
    top = Tkinter.Tk()
    top.withdraw()
    tkMessageBox.askquestion('提示：  ', prompt)
    

#获取短信信息  
def getMysqlItem(strSql,strZd):
    """
    获取sql查询结果中的第一行字段对应的内容
    Parameters:
    | getMysqlItem | SELECT * FROM `notify_record`  WHERE contact='15300207124' ORDER BY add_time DESC      |  conent   |
     """
    #strHost="172.16.6.164"
    #strUser="root"
    #strPasswd="root123"
    strHost="rr-2zejv7094o8sh96vyo.mysql.rds.aliyuncs.com"
    strUser="aixuexidball"
    strPasswd="aixuexi_2016dball"
    strDBname="managesystemv1.0"
    mysqlDB = mysqlDBUtil.dbUtil(strHost,strUser,strPasswd)
    mysqlDB.selectDb(strDBname)
    if mysqlDB.query(strSql)>0:
        result=mysqlDB.getRow(strZd)
    else:
        result="null"
    return result



#获取当前路径下文件的全路径
def getHomeDIR(imgname):
    homedir = os.getcwd().decode('GBK')
    filepath=homedir+'\\'+imgname
    return filepath

#结束进程
def taskKill(strTaskname):
    """
    taskkill the taskname
    Parameters:
    | strtaskname=<QQ.EXE>  | Title of the task      |
     """
    command = "taskkill /F /IM "+strTaskname
    os.system(command)

#产生随机身份证号
def GenneratorID():
    codelist = '110228'  # 地区项
    id = codelist + str(random.randint(1930, 2013))  # 年份项
    da = date.today() + timedelta(days=random.randint(1, 366))  # 月份和日期项
    id = id + da.strftime('%m%d')
    id = id + str(random.randint(100, 300))  # ，顺序号简单处理
    i = 0
    count = 0
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
    checkcode = {'0': '1', '1': '0', '2': 'X', '3': '9', '4': '8', '5': '7', '6': '6', '7': '5', '8': '5', '9': '3',
                 '10': '2'}  # 校验码映射
    for i in range(0, len(id)):
        count = count + int(id[i]) * weight[i]
    id = id + checkcode[str(count % 11)]  # 算出校验码
    return id

#查找字符串arg2 在字符串arg1中第几行
def FindStr(arg1, arg2):
    arg5 = 0
    arg3 = arg1.split('\n')
    for arg4 in arg3:
        arg5 = arg5 + 1
        if arg4.find(arg2) >= 0:
            arg6 = arg5
            break
        else:
            arg6 = 0
    return arg6

#保存到ini文件中
def GetIniValue(Section, Key):
    readhandle = open(filename)
    cfg.readfp(readhandle)
    try:
        value = cfg.get(Section, Key)
        readhandle.close()
    except:
        value = Default
    return value

#获取ini配置
def SetIniValue(Section, Key, Value):
    writehandle = open(filename, 'w')
    try:
        cfg.set(Section, Key, Value)
    except:
        cfg.add_section(Section)
        cfg.set(Section, Key, Value)
        cfg.write(writehandle)
    writehandle.close()

#带cookies识别url验证码
def shibieCookies(strCookies,strUrl):
    u'''接收一个目录的路径，并执行目录下的所有bat文件.例
        | shibieCookies                  | strCookies       | strUrl    |
      '''
    opener = urllib2.build_opener()
    opener.addheaders.append(('Cookie',strCookies))
    image_buff = opener.open(strUrl).read()
    im = Image.open(StringIO.StringIO(image_buff))
    # enhancer = ImageEnhance.Contrast(im)
    # im = enhancer.enhance(1.5)
    # im = im.filter(ImageFilter.DETAIL)
    # im = im.filter(ImageFilter.MedianFilter())
    im = clearColor(im)
    im = erzhihua(im)
    im = chuzaodian(im, 4, 3)
    im = xiufu(im)
    text = pytesseract.image_to_string(im)
    text = xiuzheng(text)
    return text

#识别url验证码
def shibie(url):
    u'''接收一个目录的路径，并执行目录下的所有bat文件.例
        | shibie                  | filepath                 |
       '''
    imgpath = StringIO.StringIO(urllib2.urlopen(url))
    im = Image.open(imgpath)
    #enhancer = ImageEnhance.Contrast(im)
    #im = enhancer.enhance(1.5)
    # im = im.filter(ImageFilter.DETAIL)
    # im = im.filter(ImageFilter.MedianFilter())
    im = clearColor(im)
    im = erzhihua(im)
    im = chuzaodian(im, 4, 3)
    im = xiufu(im)
    text = pytesseract.image_to_string(im)
    text = xiuzheng(text)
    return text

def clearColor(im):
    (w, h) = im.size
    for x in xrange(w):
        for y in xrange(h):
            r, g, b = im.getpixel((x,y))
            if (  b >= 195 ):  # 对蓝色进行判断
                b = 255
                g = 255
                r = 255
            im.putpixel((x, y), (r, g, b))
    return im

def erzhihua(im):
    # 二值化阈值
    threshold = 215
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    imgry = im.convert('L')
    out = imgry.point(table,'1')
    return out

def xiuzheng(text):
    # 对于识别成字母的 采用该表进行修正,且只识别大写字母
    rep = {'0': 'O',
           '1': 'I',
           '2': 'Z',
           '8': 'S'
           };
    zifu="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    text = text.strip()
    text = text.upper();
    for r in rep:
        text = text.replace(r, rep[r])
    newtext=[]
    for i in list(text):
         if i in zifu:
             newtext.append(i);
    return ''.join(newtext);

def chuzaodian(im, N, Z):
    # N: 降噪率 0 <N <8
    # Z: 降噪次数
    w, h = im.size
    for x in xrange(0, w):
        im.putpixel((x, 0), 1)
        im.putpixel((x, h - 1), 1)
    for y in xrange(0, h):
        im.putpixel((0, y), 1)
        im.putpixel((w-1, y), 1)

    for i in xrange(0, Z):
        for x in xrange(1, w - 1):
            for y in xrange(1, h - 1):
                nearDot = 0
                L = 0
                if L == im.getpixel((x, y)):
                    nearDot += 1
                if L == im.getpixel((x - 1, y - 1)):
                    nearDot += 1
                if L == im.getpixel((x - 1, y)):
                    nearDot += 1
                if L == im.getpixel((x - 1, y + 1)):
                    nearDot += 1
                if L == im.getpixel((x, y - 1)):
                    nearDot += 1
                if L == im.getpixel((x, y + 1)):
                    nearDot += 1
                if L == im.getpixel((x + 1, y - 1)):
                    nearDot += 1
                if L == im.getpixel((x + 1, y)):
                    nearDot += 1
                if L == im.getpixel((x + 1, y + 1)):
                    nearDot += 1
                if nearDot < N:
                    im.putpixel((x, y), 1)

    return im


def xiufu(im):
    (w, h) = im.size
    black = 0
    white = 1
    for x in xrange(w - 2):
        for y in xrange(h - 2):
            if black == im.getpixel((x, y)) and white == im.getpixel((x, y + 1)) and black == im.getpixel((x, y + 2)):
                im.putpixel((x, y + 1), black)
            if black == im.getpixel((x, y)) and white == im.getpixel((x + 1, y + 1)) and black == im.getpixel((x + 2, y + 2)):
                im.putpixel((x + 1, y + 1), black)
            if black == im.getpixel((x, y)) and white == im.getpixel((x + 1, y)) and black == im.getpixel((x + 2, y)):
                im.putpixel((x + 1, y), black)
    for x in xrange(w - 1):
        for y in xrange(h - 1):
            if x>0 and y>0 and black == im.getpixel((x, y)) and black == im.getpixel((x, y + 1)) and white == im.getpixel((x+1, y)) and white == im.getpixel((x+1, y + 1)) and white == im.getpixel((x-1, y)) and white == im.getpixel((x-1, y + 1)):
                im.putpixel((x+1, y ), black)
                im.putpixel((x+1, y + 1), black)
            if x>0 and y>0 and  black == im.getpixel((x, y)) and black == im.getpixel((x+1, y)) and white == im.getpixel(
                    (x , y+1)) and white == im.getpixel((x + 1, y + 1)) and white == im.getpixel(
                    (x , y-1)) and white == im.getpixel((x +1, y -1)):
                im.putpixel((x , y+1), black)
                im.putpixel((x + 1, y + 1), black)


    return im





if __name__=='__main__':
    url = "http://172.20.3.3:8001/zh-cn/captcha/image/b5c1fc6343fe9eeabd528589882cb576305bce9c/"
    text = shibie(url)
    print text