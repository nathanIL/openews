#    GNU Makefile to cofigure various parts of the software
# ============================================================
# The available targets are:
# 1) clean: will remove all created virtualenvironments as well as the NLTK data.
# 2) configure-test: will configure (virtualenv & dependencies) for a development environment (running tests).
# 3) configure-prod: will configure (virtualenv & dependencies) for a production environment.
# 4) test: will run the test. call 'configure-test' before.

clean:
	rm -rf nltk_data;
	rm -rf venv;
	find . -type d -name "__pycache__" | xargs rm -rf
	find . -type f -name "*.py[cod]" | xargs rm -f
	rm -f /tmp/openews*

configure-test:
	virtualenv --clear -p python3 venv;
	source venv/bin/activate && pip install -r requirements-dev.txt;
	source venv/bin/activate && python -m nltk.downloader -d nltk_data stopwords punkt

configure-prod:
	virtualenv --clear -p python3 venv;
	source venv/bin/activate && pip install -r requirements-prod.txt;
	source venv/bin/activate && python -m nltk.downloader -d nltk_data stopwords punkt

test:
	source venv/bin/activate && (export OPENEWS_DEVELOPMENT_ENV="true"; nosetests -v -s tests/test_*; unset OPENEWS_DEVELOPMENT_ENV);

test-language:
	source venv/bin/activate && (export OPENEWS_DEVELOPMENT_ENV="true"; nosetests -v -s tests/language_*; unset OPENEWS_DEVELOPMENT_ENV);