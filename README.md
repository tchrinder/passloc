# passloc
# password locker program
# python3
## version 1.0

## Installation 
#### From Linux terminal or Windows command line:

git clone -b development https://github.com/tchrinder/passloc.git
cd passloc
pip install -r requirements.txt

## Usage

               passloc.py -n filename -p password
               passloc.py -f filename -p password
               
        -n --new - create a new passloc file
        -f --file - access existing passloc file
        -p --password - password for passloc file, optional
        
## Examples

    python passloc.py -n container
    python passloc.py -n container -p 'password'
    python passloc.py -f container

### PyCrypto errors on Windows

Some newer versions of Python3 require additional software in order
to build PyCrypto's binary extensions on Windows

Refer to https://packaging.python.org/extensions/#building-binary-extensions
to find and install the required software before trying the following command

pip install PyCrypto