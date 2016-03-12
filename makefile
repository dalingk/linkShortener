bottle_dir=bottle
html_dir=html

all: html bottle 
	sudo service uwsgi reload

html: sw_style.css stats.js

bottle: links.tpl new.tpl app.py layout.tpl login.tpl register.tpl

sw_style.css:
	cp sw_style.css $(html_dir)

stats.js:
	cp stats.js $(html_dir)

links.tpl:
	cp links.tpl $(bottle_dir)

new.tpl:
	cp new.tpl $(bottle_dir)

layout.tpl:
	cp layout.tpl $(bottle_dir)

login.tpl:
	cp login.tpl $(bottle_dir)

register.tpl:
	cp register.tpl $(bottle_dir)

app.py:
	cp app.py $(bottle_dir)
