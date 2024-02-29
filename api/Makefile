CODE=src
TESTS=tests

format:
	black ${CODE} ${TESTS}
	isort ${CODE} ${TESTS}

test:
	pytest --cov-report html --cov=${CODE} ${CODE} ${TESTS}

lint:
	pylint --recursive=y --disable=R,C ${CODE} ${TESTS}
	black --check ${CODE} ${TESTS}
	isort --check-only ${CODE} ${TESTS}

lintci:
	pylint --recursive=y --disable=W,R,C ${CODE} ${TESTS}
	black --check ${CODE} ${TESTS}
	isort --check-only ${CODE} ${TESTS}


run:
	uvicorn main:app --reload
