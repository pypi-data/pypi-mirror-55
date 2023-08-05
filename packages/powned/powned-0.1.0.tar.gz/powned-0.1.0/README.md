# Powned
Powned is a python packaged designed to check if your password was recovered in a data breach.  
Harnessing the power of [haveibeenpwned](https://haveibeenpwned.com/) your query is sent safely and securely using k-anonymity practices.

## Installation
Windows, OS X, and Linux
```shell
> pip install powned
```

## Usage Example
```pycon
>>> import powned
>>> powned.check("password1")
21345  # "password1" recovered in 21345 breaches
```

## Development Setup
For when you want to work on Powned.

Clone this repository
```shell
> git clone https://github.com/alexmacniven/powned.git
```
Create a virtual environment
```shell
> virtualenv venv
> ./venv/scripts/activate
```
Use `pip` to install in editable mode with development requirements
```shell
> pip install -e '.[dev]'
```
Run the provided test suite
```shell
> python -m pytest
```

## Release History
 - 0.1.0
   - Initial release
   - Adds password `check` functionality

## Meta
Alex Macniven - [@alex_macniven](https://twitter.com/alex_macniven) - [@gmail](mailto:macniven.ap@gmail.com)  
Distributed under the MIT license.
