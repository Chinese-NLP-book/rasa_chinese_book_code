.PHONY: install
install:
	pip install rasa-x --extra-index-url https://pypi.rasa.com/simple
	pip install -r ./requirements.txt

.PHONY: smoke_test
smoke_test: clean_models
	(cd Chapter02 && rasa train)
	(cd Chapter03 && rasa train)
	(cd Chapter04 && rasa train)
	(cd Chapter05 && rasa train)
	(cd Chapter06 && rasa train)
	(cd Chapter07 && rasa train)
	(cd Chapter08 && rasa train)
	(cd Chapter09 && rasa train)

	$(MAKE) clean_models

.PHONY: clean_models
clean_models:
	(cd Chapter02 && rm -rf models .rasa)
	(cd Chapter03 && rm -rf models .rasa)
	(cd Chapter04 && rm -rf models .rasa)
	(cd Chapter05 && rm -rf models .rasa)
	(cd Chapter06 && rm -rf models .rasa)
	(cd Chapter07 && rm -rf models .rasa)
	(cd Chapter08 && rm -rf models .rasa)
	(cd Chapter09 && rm -rf models .rasa)

.PHONY: clean
clean:
	# remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	# remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: dev
dev:
	npm install -g markdownlint-cli
	pip install black
	pip install flake8
	npm i -g @lint-md/cli

.PHONY: dev_check
dev_check:
	flake8 --ignore=E501 Chapter0*
	black --check Chapter0*
	markdownlint --disable MD013 MD034 MD024 -- README.md **/README.md
	lint-md -f */README.md
