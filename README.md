# stockeasy
Quick and Easy Stock Portfolio Analysis - FOR ENTERTAINMENT PURPOSES ONLY!!

### Note
I use Docker for enviroment management; as such, my build process will deviate from more classical approaches. 

```
docker build -f ./container/dockerfile . -t stockeasy:develop

pip install -r requirements_dev.txt
python setup.py sdist bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
pip install --index-url https://test.pypi.org/simple/ stockeasy
```


### References
https://towardsdatascience.com/build-your-first-open-source-python-project-53471c9942a7
https://medium.com/@michaelekpang/creating-a-ci-cd-pipeline-using-github-actions-b65bb248edfe

Python Testing with pytest ISBN 978-1-68050-240-4
The Wall Street Journal Guide To Information Graphics ISBN 978-0-393-34728-9