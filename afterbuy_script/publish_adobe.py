import requests
import json
import os
import sys

form_url = sys.argv[1]


def user_apps(token):
    url = 'https://build.phonegap.com/api/v1/me/?auth_token=%s' % token
    r = requests.get(url)
    if r.status_code < '300':
        return json.loads(r.content).get("apps", None)
    return None


def delete_other_apps(token):
    apps = user_apps(token)
    if apps:
        for app_data in apps['all']:
            app_id = app_data["id"]
            url = 'https://build.phonegap.com/api/v1/apps/%s/?auth_token=%s'\
                                                     % (app_id, token)
            requests.delete(url)


def get_phonegap_token(auth):
    url = 'https://build.phonegap.com/token'
    r = requests.post(url, auth=auth)
    if r.status_code < '300':
        return json.loads(r.content).get("token", None)
    return None


def get_app_id(app_path, auth):
    files = {'file': open(app_path, 'rb')}
    data = json.dumps({"create_method": "file", "package":\
            "com.alunny.apiv1", "version": "0.1.0", "title": "API V1 App"})
    url = 'https://build.phonegap.com/api/v1/apps/'
    r = requests.post(url, files=files, auth=auth, data={'data': data})
    os.remove(app_path)
    if r.status_code < '300':
        return json.loads(r.content)["id"]


app_path = 'afterbuy_script/afterbuy.zip'
auth = ('support@gladminds.co', 'gladminds123')
token = get_phonegap_token(auth)
delete_other_apps(token)

if os.path.isfile(app_path) and token:
    app_id = get_app_id(app_path, auth)

r = None
counter = 0 
while not r or r.status_code > 299 or counter < 50:
    print "getting file from buildserver"
    print counter
    counter = counter + 1
    url = "https://build.phonegap.com/api/v1/apps/"\
                 + str(app_id) + "/android/?auth_token=" + token
    r = requests.get(url=url)
if form_url == "https://api-qa.gladmindsplatform.co/gm/":
    app_name = "afterbuy_script/qa_afterbuy.apk"
else:
    app_name = "afterbuy_script/prod_afterbuy.apk"

if os.path.isfile(app_name):
    os.remove(app_name)

s = open(app_name, 'w')
s.write(r.content)
