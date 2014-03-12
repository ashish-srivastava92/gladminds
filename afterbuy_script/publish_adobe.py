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


def get_build_file(app_id, build, token):
    r = None
    counter = 0
    while not r or r.status_code > 299 or counter < 50:
        print "getting {0} exec from build server".format(build)
        counter = counter + 1
        url = "https://build.phonegap.com/api/v1/apps/{0}/{1}/?auth_token={2}"\
                                                .format(app_id, build, token)
        r = requests.get(url=url)
    return r


def create_build_file(response, app_name):
    if os.path.isfile(app_name):
        os.remove(app_name)
    s = open(app_name, 'w')
    s.write(r.content)


if form_url == "https://api-qa.gladmindsplatform.co/gm/":
    auth = ('support@gladminds.com', 'gladminds123')
    key_prefix = "qa"
else:
    auth = ('support@gladminds.co', 'gladminds123')
    key_prefix = "prod"


app_path = 'afterbuy_script/afterbuy.zip'
token = get_phonegap_token(auth)
delete_other_apps(token)

if os.path.isfile(app_path) and token:
    app_id = get_app_id(app_path, auth)
    r = get_build_file(app_id, "android", token)
    create_build_file(r, "afterbuy_script/{0}_{1}_afterbuy.apk"\
                                        .format(key_prefix, "android"))

    r = get_build_file(app_id, "ios", token)
    create_build_file(r, "afterbuy_script/{0}_{1}_afterbuy.apk"\
                                        .format(key_prefix, "ios"))
