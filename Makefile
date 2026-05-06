.PHONY: clean build upload github-push
.DEFAULT_GOAL := help
BRANCH ?= main

-include .env
export



clean:
	@echo "Cleaning __pycache__..."
	find kyodo -type d -name "__pycache__" -exec rm -rf {} +
	find tests -type d -name "__pycache__" -exec rm -rf {} +

	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf *.dist-info

	@echo "Done."

build:
	@echo "Building source distribution..."
	python3 setup.py sdist

upload: clean build
	@echo "Uploading package..."
	@if [ -z "$(PYPI_TOKEN)" ] || [ "$(PYPI_TOKEN)" = "" ]; then \
		read -r -p "Enter PyPI token: " token < /dev/tty; \
		TWINE_PASSWORD=$$token twine upload dist/*; \
	else \
		TWINE_PASSWORD=$(PYPI_TOKEN) twine upload dist/*; \
	fi


push:
	@echo "Syncing with remote (branch: $(BRANCH))..."
	@git add .
	@git commit -m "update" || echo "Nothing to commit"
	@echo "Fetching..."
	git fetch origin $(BRANCH)
	@echo "Rebasing..."
	git rebase origin/$(BRANCH) || (echo "Rebase failed - aborting" && git rebase --abort && exit 1)
	@echo "Pushing..."
	git push origin $(BRANCH)


test:
	@if [ -f tests/.env ]; then \
		set -a; \
		. tests/.env; \
		set +a; \
	fi; \
	PYTHONPATH=. python3 -m tests.$(n)

help:
	@echo ""
	@echo "\033[1;32mAvailable commands:\033[0m"
	@echo "  make clean         - Clean cache and build artifacts"
	@echo "  make build         - Build source distribution"
	@echo "  make upload        - Clean, build and upload package to PyPI"
	@echo "  make push          - Commit, rebase and push to GitHub (BRANCH=x, default: main)"
	@echo "  make test n=x  - Run test module (example: n=test or n=api.test_users) (from tests/ folder)"
	@echo "  make help          - Show this help message"