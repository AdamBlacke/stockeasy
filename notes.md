```
docker build -f ./container/dockerfile . -t stockeasy:develop
docker run -v C:\Users\ablac\OneDrive\Documents\stockeasy\:/stockeasy -it stockeasy:develop 
python3 -m pip install -e .
flake8 --ignore=F401

pip install -r requirements_dev.txt
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install --index-url https://test.pypi.org/simple/ stockeasy
```


### References
https://towardsdatascience.com/build-your-first-open-source-python-project-53471c9942a7
https://medium.com/@michaelekpang/creating-a-ci-cd-pipeline-using-github-actions-b65bb248edfe
https://towardsdatascience.com/how-to-get-stock-data-using-python-c0de1df17e75

Python Testing with pytest ISBN 978-1-68050-240-4
The Wall Street Journal Guide To Information Graphics ISBN 978-0-393-34728-9