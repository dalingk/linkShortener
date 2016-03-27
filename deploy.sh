#!/bin/sh
bottle_dir='bottle'
bottle_files='app.py links.tpl layout.tpl login.tpl new.tpl register.tpl'
static_dir='html'
static_files='sw_style.css stats.js'
cp -iu $bottle_files $bottle_dir
cp -iu $static_files $static_dir
cd $bottle_dir
chmod 444 $bottle_files
cd ..
cd $static_dir
chmod 444 $static_files
read -p "Restart uwsgi? " yn
if echo $yn | grep -iq "^y"; then
    sudo service uwsgi reload
fi
