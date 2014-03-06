import requests


auth = ('support@gladminds.co', 'gladminds123')
url = "https://build.phonegap.com/token"
r = requests.post(url, auth=auth)
print r


url = "https://build.phonegap.com/api/v1/apps/"+"807756"+"/android/?auth_token="+"A3fcRMdraJNCqEqzyKqS"
print url
r = requests.get(url = url)
print r
