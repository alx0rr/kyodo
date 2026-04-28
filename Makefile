.PHONY: clean build upload

clean:
	@echo "Cleaning __pycache__..."
	find kyodo -type d -name "__pycache__" -exec rm -rf {} +

	@echo "Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf *.dist-info

	@echo "Done."


build:
	@echo "Building source distribution..."
	python3 setup.py sdist

pypi-upload: clean build
	@echo "Uploading package..."
	twine upload dist/*


github-push:
	@echo "Pushing to main..."
	git add .
	git commit -m "update" || echo "Nothing to commit"
	git push origin main