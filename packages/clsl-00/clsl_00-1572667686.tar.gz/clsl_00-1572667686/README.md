# clsl_00

## Cheat sheet

```
python3 -m venv venv
source venv/bin/activate

pip install --upgrade setuptools wheel nose twine keyring

keyring set https://upload.pypi.org/legacy/ luzi82
keyring set https://test.pypi.org/legacy/ luzi82

rm -rf dist
python3 setup.py sdist bdist_wheel

python3 -m twine upload -u luzi82 --repository-url https://test.pypi.org/legacy/ dist/*
python3 -m twine upload -u luzi82 dist/*
deactivate
```
