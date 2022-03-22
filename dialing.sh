#!/bin/bash
#Author: Wang DeJi
#Date: 2021/09/09 00:30
#Version: 1.2

Auth_User=""
Auth_Pass=""

TempFile=$(mktemp)
TempFile2=$(mktemp)

#WebAuth 1 step
echo "Info: Login step 1."
curl -s -D $TempFile captive.apple.com > /dev/null
if [ -z "$(cat $TempFile | grep "192.168.99.5")" ]; then
	echo "Error: No Run in School InterNal."
	rm -rf $TempFile
	rm -rf $TempFile2
	exit
fi
curl -s -D $TempFile -c $TempFile2 -L "192.168.99.5/portal" > /dev/null

#Get Sub Url
SubUrl=$(cat "$TempFile" | grep "/PortalServer/portal.jsp" | sed 's/Location: //')
if [ -z "$SubUrl" ]; then
	echo "Error: Get WebSystem Auth SubUrl Fail."
	rm -rf $TempFile
	rm -rf $TempFile2
	exit
fi

echo "Info: Get Login Cooking......."
#Get JSESSIONID Cookie
JSESSIONID=$(cat "$TempFile2" | grep 'JSESSIONID' | awk '{print $6"="$7}')

#Get XSRF-TOKEN
Return_Web=$(curl -s -d "customPageConfigId=4028e3856a9b45fd016ae2cb57c52060" --cookie "$JSESSIONID" 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!getCustomPageConfig.action')
if [ -z "$Return_Web" ]; then
	echo "Error: Get WebSystem XSRF-TOKEN Fail."
	rm -rf $TempFile
	rm -rf $TempFile2
	exit
fi

X_XSRF_TOKEN=${Return_Web:41:32}

echo "Info: Login WebAuth now...... step 2"
#Login WebAuth step 2
Return_Web=$(curl -s -c $TempFile --cookie "$JSESSIONID; XSRF-TOKEN=$X_XSRF_TOKEN" -d "authType=&userName="$Auth_User"&password="$Auth_Pass"&validCode=&valideCodeFlag=false&authLan=zh_CN&hasValidateNextUpdatePassword=true&rememberPwd=true&browserFlag=zh&hasCheckCode=false&checkcode=&hasRsaToken=false&rsaToken=&saveTime=14&autoLogin=false&userMac=&isBoardPage=false&disablePortalMac=false&overdueHour=0&overdueMinute=0&isAccountMsgAuth=&validCodeForAuth=&isAgreeCheck=0" -H "X-XSRF-TOKEN: $X_XSRF_TOKEN" -H "X-Requested-With: XMLHttpRequest" -H "Content-Type: application/x-www-form-urlencoded; charset=UTF-8" 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!login.action')

if [[ ${Return_Web} =~ '"accessStatus":200' ]]; then
	
	#Login Ok Step Good End A
	X_XSRF_TOKEN=$(cat $TempFile | grep 'XSRF-TOKEN' | awk '{print $7}')
	Return_Web=$(curl -s -b $TempFile -d "browserFlag=zh&userMac=" -H "X-XSRF-TOKEN: $X_XSRF_TOKEN" 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!syncPortalAuthResult.action')	
	while [ $(echo $Return_Web | wc -c) -gt $(echo $Return_Web | awk -F '"portalAuthStatus":0' '{print $1}' | wc -c) ]; do
		sleep 3
		Return_Web=$(curl -s -b $TempFile -d "browserFlag=zh&userMac=" -H "X-XSRF-TOKEN: $X_XSRF_TOKEN" 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!syncPortalAuthResult.action')
	done

	echo "Info: School InterNet Auth Success."
	#Login Ok Step End While
	Return_Web=$(curl -s -b $TempFile -d "browserFlag=zh" -H "X-XSRF-TOKEN: $X_XSRF_TOKEN" 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!getBindPolicy.action')
	while [ $(echo $Return_Web | wc -c) -gt $(echo $Return_Web | awk -F '"message":null' '{print $1}' | wc -c) ]; do
		sleep 60
		Return_Web=$(curl -s -b $TempFile -d "browserFlag=zh" -H "X-XSRF-TOKEN: $X_XSRF_TOKEN" 'http://192.168.99.5/PortalServer/Webauth/webAuthAction!getBindPolicy.action')
	done

	#Exit ProgRam
	echo "Info: WebAuth InterNet Offline."
	rm -rf $TempFile
	rm -rf $TempFile2
	exit
fi

#Login Fail Step Bad End B
echo "Error: Login Fail, Raw Json Data:"
echo "$Return_Web"
rm -rf $TempFile
rm -rf $TempFile2
exit