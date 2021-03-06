#!/bin/sh
# Script to create phonegap app
cd afterbuy_script
sudo rm -r afterbuy
cd afterbuy-ui
git pull
cd ../
phonegap create afterbuy -n afterbuy -i com.gladminds.afterbuy
sudo cp -r afterbuy-ui/* afterbuy/www 
sudo python parse_afterbuy.py $1  
cd afterbuy 
cd ../
zip -r afterbuy afterbuy
cd ../
bin/python afterbuy_script/publish_adobe.py $1
bin/python afterbuy_script/apk_upload.py $1
exit 0
