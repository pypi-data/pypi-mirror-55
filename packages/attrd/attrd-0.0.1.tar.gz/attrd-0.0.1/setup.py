import setuptools
from pathlib import Path

readme_path = Path('./README.md')
long_description = readme_path.read_text()
description = long_description.split('\n', 1)[0]

setuptools.setup(
    name='attrd',
    version='0.0.1',
    author='Filantus',
    author_email='filantus@mail.ru',
    url='https://pypi.org/project/attrd/',
    description=description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    py_modules=['attrd'],
    packages=setuptools.find_packages(),
    license='GPL',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
    ],
)
