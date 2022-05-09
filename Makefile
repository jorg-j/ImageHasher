#.ONESHELL:

#.PHONY: install

venv: env/touchfile


env/touchfile: requirements.txt
	test -d env || python3 -m venv env
	. env/bin/activate; pip3 install -r requirements.txt
	touch env/touchfile

deepclean:
	rm -r data
	rm *.db

run: venv
	. env/bin/activate; python3 imhash.py