from bs4 import BeautifulSoup
import requests

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
try:
    requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
except AttributeError:
    # no pyopenssl support used / needed / available
    pass

url='https://easprep.osce.gob.pe/portaltribunal-uiwd-pub/ControllerServlet'
cookie={'JSESSIONID':'cGmELYffoEGrRIFMC02nwfr6.31343ada-59ff-3a71-b141-1abc3a553f94'}
page=requests.get(url,cookies=cookie,verify=False)

soup=BeautifulSoup(page.text,'html')

submit_captcha=requests.post(url,cookies=cookie,verify=False)
response=BeautifulSoup(submit_captcha.text,'lxml')

print(response)