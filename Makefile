PROGRAM = gch.py gdiff.py 
SRC = src/arg.py src/diff.py src/git/branch.py src/git/checkout.py src/git/commit.py src/git/init.py src/git/log.py src/git/ls_files.py src/git/pull.py src/git/push.py src/git/remote.py src/git/reset.py src/git/status.py src/issues.py src/log.py src/parse.py src/proc.py src/qs.py src/util.py src/version.py

main: gch.py $(SRC)
	python gch.py

install:
	pip install -r requirements.txt

pep: $(PROGRAM) $(SRC)
	autopep8 -i gch.py gdiff.py src/*.py

flake: $(PROGRAM) $(SRC)
	flake8 --ignore=E501,E241 --exclude=__init__.py,build.py gch.py gdiff.py src/*.py

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
	pyinstaller gdiff.py --onefile
	rm -r build
	rm gch.spec

build:	$(PROGRAM) $(SRC)
	python build.py
