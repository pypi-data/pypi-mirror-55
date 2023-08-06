# Installing apep

## Installing with pip

In an existing python project, pip install **apep**.

```
pip install apep
```

## Development

### Setup

.. is also a fine way to install **apep**, using GIT as a starting project.

```bash
cd elioway
git clone https://gitlab.com/elioway/elioangels.git
cd elioangels
git clone https://gitlab.com/elioangels/apep.git
cd apep
virtualenv --python=python3 venv-apep
source venv-apep/bin/activate
pip install -r requirements/local.txt
```

**Run the tests:**

```bash
find . -name '*.pyc' -delete
find . -name '__pycache__' -delete
py.test -x
```

### Publish

Activate the virtualenv.

```
python3 setup.py sdist bdist_wheel
twine upload dist/*
# Enter YOUR-USERNAME and YOUR-PASSWORD
```

Testing it:

```
pip install apep
```

**Test Publish**

```
python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
# Enter YOUR-USERNAME and YOUR-PASSWORD
cd some/test/folder
virtualenv --python=python3 venv-apep
source venv-apep/bin/activate
# or
source venv-apep/bin/activate.fish
python3 -m pip install --index-url https://test.pypi.org/simple/ apep
```
