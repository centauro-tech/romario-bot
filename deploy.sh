#!/bin/bash

mkdir build
pip install -r requirements.txt -t build/
cp -R src/* build

echo "deploying $lambda >>>>>>>>>"
cd build
zip -qr ../src.zip *
cd ../

### Create the role for the lambda to assume
role="lambda_basic_execution"
function_name="$1"
handler_name="main.handler"
package_file=./src.zip

### Update the function
runtime=python2.7
aws lambda update-function-code \
  --function-name $function_name \
  --zip-file fileb://$package_file \
  --region us-east-1


rm src.zip
rm -rf build

echo 'End of the deploy >>>>>>>>>'

#cd html
#aws s3 cp . s3://agilemetrics.vivareal.com/ --recursive --exclude "src/*" --exclude "*/.DS_Store" --exclude ".DS_Store"