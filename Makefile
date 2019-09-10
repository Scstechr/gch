PROGRAM = gch.py gdiff.py 
SRC = src/arg.py src/diff.py src/git.py src/issues.py src/log.py src/parse.py src/qs.py src/util.py src/version.py

main: $(PROGRAM) $(SRC)
	python gch.py

install:
	pip install -r requirements.txt

pep: $(PROGRAM) $(SRC)
	autopep8 -i *.py
	autopep8 -i src/*.py

flake: $(PROGRAM) $(SRC)
	flake8 --ignore=E501,E241 *.py
	flake8 --ignore=E501,E241 src/*.py

commit:
	gch -cv

pfc: $(PROGRAM) $(SRC)
	autopep8 -i *.py
	autopep8 -i src/*.py
	flake8 --ignore=E501,E241 *.py
	flake8 --ignore=E501,E241 src/*.py
	gch -cv

dist: $(PROGRAM) $(SRC)
	pyinstaller gch.py --onefile
	rm -r build
	rm gch.spec

	
