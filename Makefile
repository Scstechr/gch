main:
	python gch.py

install:
	pip install -r requirements.txt

pep:
	autopep8 -i *.py
	autopep8 -i src/*.py

commit:
	gch -cv

pfc:
	autopep8 -i *.py
	autopep8 -i src/*.py
	flake8 --ignore=E501,E241 *.py
	flake8 --ignore=E501,E241 src/*.py
	gch -cv

flake:
	
