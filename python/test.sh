#!/bin/bash
now=$(date +%Y%m%d%H%M)
echo $now

sed -i -e "s/version=.*\"/version=$now\"/g" ./public_html/dist/js/crypto_info.js
sed -i -e "s/js?version=.*\"/js?version=$now\"/g" ./public_html/index.html
sed -i -e "s/version=.*\"/version=$now\"/g" ./public_html/dist/js/crypto_info_result.js
sed -i -e "s/js?version=.*\"/js?version=$now\"/g" ./public_html/index2.html
sed -i -e "s/version=.*\"/version=$now\"/g" ./public_html/dist/js/crypto_info_star.js
sed -i -e "s/js?version=.*\"/js?version=$now\"/g" ./public_html/star.html
