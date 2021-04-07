clean:
	find . -name "*.pyc" -exec rm -f {} \;
	find . -name "*.pyo" -exec rm -f {} \;
	find . -name "*.py[co]" -o -name __pycache__ -exec rm -rf {} +
