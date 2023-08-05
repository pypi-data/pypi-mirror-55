# ML-toolkit

# Python package basics
    - Create Source distribution: `python setup.py sdist`
    - Install package: `pip install ml-toolkit-1-0.0.1.tar.gz` (installs package into python site-packages)
    - Create Wheel: `python setup.py bdist_wheel`
    - Upload to pypi:
        - Test server: `twine upload --repository-url https://test.pypi.org/legacy/ -r ml-toolkit-prajit dist/ml-toolkit-1-0.0.1.tar.gz`
        - pypi.org: `twine upload --repository-url https://upload.pypi.org/legacy/ -r ml-toolkit-prajit dist/ml-toolkit-1-0.0.1.tar.gz` 
    
    