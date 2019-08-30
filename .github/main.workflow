name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      max-parallel: 4
      matrix:
        python-version: [2.7, 3.5, 3.6, 3.7]

    steps:
    - uses: actions/checkout@v1
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v1
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip wheel
        pip install -U -r requirements-test.txt -r requirements-ci.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8
    - name: Test with pytest
      run: |
        pip install pytest
        py.test --cov=translation_finder translation_finder README.rst