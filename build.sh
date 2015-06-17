python setup.py sdist --format=zip

cd dist/

rm -rf gladminds-0.0.1

unzip gladminds-0.0.1.zip

cd gladminds-0.0.1/

zip build.zip -r .* -x "../*" "*~*"

mv build.zip ../../

cd ../../

bin/fab deploy_to_dev_environment
