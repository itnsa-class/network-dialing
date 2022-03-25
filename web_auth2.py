import sys
import io
import urllib.request
import http.cookiejar


sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')

#登录时需要POST的数据
data = {'userName':'201711101', 
        'password':'Skills39', 
        'authType':'',
        'validCode':'zh_CN',
        'hasValidateNextUpdatePassword':'true',
        'rememberPwd':'false',
        'browserFlag':'zh',
        'hasCheckCode':'false',
        'checkcode':'',
        'hasRsaToken':'false',
        'rsaToken':'',
        'autoLogin':'false',
        'userMac':'',
        'isBoardPage':'false',
        'disablePortalMac':'false',
        'overdueHour':'0',
        'overdueMinute':'0',
        'isAccountMsgAuth':'',
        'validCodeForAuth':'',
        'isAgreeCheck':'0',
}
post_data = urllib.parse.urlencode(data).encode('utf-8')

#设置请求头
headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

login_url = 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!login.action'

#构造登录请求
req = urllib.request.Request(login_url, headers = headers, data = post_data)
#构造cookie
cookie = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie))

resp = opener.open(req)
resp = opener.open(req)

Result = resp.read().decode('utf-8')


