#!/bin/bash
now=$(date +%Y%m%d%H%M)
echo $now

sed -i -e "s/version=.*\"/version=$now\"/g" $HOME/kousotsu-py.info/public_html/dist/js/crypto_table2.js
sed -i -e "s/js?version=.*\"/js?version=$now\"/g" $HOME/kousotsu-py.info/public_html/index.html