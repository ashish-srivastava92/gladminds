#!/bin/sh
# Script to create phonegap app
cd afterbuy_script
rm -r afterbuy
phonegap create afterbuy -n afterbuy -i com.gladminds.afterbuy
git clone git@git.labs.hashedin.com:gladminds/afterbuy.git afterbuy-ui
cp -r afterbuy-ui/* afterbuy/www 
python parse_afterbuy.py $1  
cd afterbuy 
cd ../
zip -r afterbuy afterbuy
cd ../
bin/python afterbuy_script/publish_adobe.py $1
bin/python afterbuy_script/apk_upload.py $1
exit 0
