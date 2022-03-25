import time

from selenium import webdriver

usernames = "17030550120" 

password1 = "166113" 

driver=webdriver.Chrome("C:\Program Files\Google\Chrome\Application\chromedriver.exe"); 
time.sleep(1)
# driver.get("https://www.baidu.com");
driver.get("http://192.168.99.5/PortalServer/customize_new/1558583138204/phone/auth.jsp?isPasscode=N&browserFlag=zh&folderName=1558583138204/phone&httpsFlag=N&publicBarcodeEncode=null&authSuccess=3&redirectUrl=&urlParameter=&currentTime=1601254051542&authislogoff=true");

driver.find_element_by_id("username").click() 

driver.find_element_by_id("username").send_keys(usernames)

time.sleep(1)

driver.find_element_by_id('_password').click() 

time.sleep(1)

driver.find_element_by_css_selector("input[emptytip='密码']").send_keys(password1)

time.sleep(1)

driver.find_element_by_id("loginBtn").click() 

try:
    while driver.find_element_by_id("loginBtn") :
        time.sleep(2);
        print(1);
except:
    time.sleep(1);
    print('Auth Success');
    
driver.close()
