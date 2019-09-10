main:
	python gch.py

install:
	pip install -r requirements.txt

commit:
	autopep8 -i gch.py
	autopep8 -i gdiff.py
	autopep8 -i src/git.py
	autopep8 -i src/arg.py
	autopep8 -i src/diff.py
	autopep8 -i src/git.py
	autopep8 -i src/issues.py
	autopep8 -i src/log.py
	autopep8 -i src/parse.py
	autopep8 -i src/qs.py
	autopep8 -i src/util.py
	autopep8 -i src/version.py
	gch -cv

