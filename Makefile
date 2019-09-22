
main:
	python gch.py

install:
	pip install -r requirements.txt

pep:
	autopep8 -i gch.py src/*.py

flake:
	flake8 --ignore=E501,E241 --exclude=__init__.py,build.py gch.py src/*.py

commit:
	gch -cv

pfc:
	autopep8 -i *.py
	autopep8 -i src/*.py
	flake8 --ignore=E501,E241 *.py
	flake8 --ignore=E501,E241 src/*.py
	gch -cv

dist:
	pyinstaller gch.py --onefile
	rm -r build
	rm gch.spec

build:
	python build.py
