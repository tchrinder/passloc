#! python3
"""This module provides the logic and the command
line interface for the passloc program"""

import sys
import os
import getopt
import getpass
import lockercrypto

def usage():
    """Prints the usage of the program and terminates"""
    print('''passloc - password management tool
        
        Usage: passloc.py -n filename -p password
               passloc.py -f filename -p password
        -n --new - create a new passloc file
        -f --file - access existing passloc file
        -p --password - password for passloc file, optional
        
        ''')
    sys.exit(0)

def getpassword(confirm):
    """Prompts and returns user password, asks for confirmation
    if new file"""
    password = getpass.getpass()
    if confirm:
        #return empty string if confirmation fails
        if password != getpass.getpass('Confirm password: '):
            print('Passwords don\'t match, try again.')
            return ''
    return password

def select_service(pd):
    """Print credentials for a given service"""
    print('')
    service = input('Enter a service (ie gmail, amazon, netflix): ')
    try:
        #prints and formats a table with appropriate headers
        print('{: >15} {: >15} {: >30}'.format('Service','Username','Password'))
        print(''.ljust(65,'-'))
        result = '{: >15} {: >15} {: >30}'.format(
            service,pd[service].split(':')[0],pd[service].split(':')[1])
        print(result)
        print('')
    #catch non-existent service inputs
    except KeyError:
        print('SERVICE NOT FOUND')
        print('')
    
def select_all(pd):
    """Print credentials for all stored services"""
    print('')
    #prints and formats table
    print('{: >15} {: >15} {: >30}'.format('Service','Username','Password'))
    print(''.ljust(65,'-'))
    for key,value in pd.items():
        print('{: >15} {: >15} {: >30}'.format(
            key,value.split(':')[0],value.split(':')[1]))
    print('')

def delete_service(pd):
    """Delete credentials for a given service"""
    service = input('Enter a service (ie gmail, amazon, netflix): ')
    try:
        del pd[service]
    #catch non-existent service inputs
    except KeyError:
        print('SERVICE NOT FOUND')
        print('')
        return
    #notify user
    print(service + ' credentials deleted')
    print('')

def delete_all(pd):
    """Delete credentials for all stored services"""
    #user confirmation
    confirmation = input('Are you sure you want to delete all credentials? [y/n]: ')
    if confirmation.lower() == 'y':
        pd.clear()
        #notify user
        print('Locker cleared')
    else:
        print('Deletion aborted')
    print('')
    
def add_service(pd):
    """Add or update credentials for a given service"""
    print('')
    service = input('Enter a service (ie gmail, amazon, netflix): ')
    username = input('Enter service username: ')
    password = input('Enter service password: ')
    pd[service] = username + ':' + password
    print('')
    
def run_locker(filename, password, newfile):
    """Handles user interaction and functions of passloc program"""
    #load locker or generate new one
    if not newfile:
        password_dictionary = lockercrypto.decrypt(filename, password)
    else:
        password_dictionary = {}
    
    print('')
    print('Password Locker initialization successful')
    print('')
    
    #locker functions
    while True:
        print('''Please select an option:
        [1] [list] credentials for a specific service
        [2] list [all] credentials
        [3] [del]ete credentials for a specific service
        [4] [delete] all credentials
        [5] [add] or update credentials for a service
        [exit]
        ''')
        
        choice = input('Selection: ')
        #process user selections
        if choice in ("1","list"):
            select_service(password_dictionary)
        elif choice in ("2", "all"):
            select_all(password_dictionary)
        elif choice in ("3", "del"):
            delete_service(password_dictionary)
        elif choice in ("4", "delete"):
            delete_all(password_dictionary)
        elif choice in ("5", "add"):
            add_service(password_dictionary)
        elif choice == "exit":
            lockercrypto.encrypt(filename, password, password_dictionary)
            print('Successfully saved locker into file ' + filename)
            sys.exit(0)
        else:
            print('INVALID SELECTION')

def main():
    """Starts passloc, parses user options and arguments"""
    #check arguments
    if len(sys.argv[1:]) < 2:
        usage()
    
    #parse user options
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:f:p:",
        ["help", "new", "file","password"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        
    password = ''
    file = ''
    newfile = False
    
    #process user options and arguments
    for o,a in opts:
        if o in("-p","--password"):
            password = a
        elif o in("-n","--new"):
            file = a
            newfile = True
        elif o in("-f","--file"):
            file = a
        else:
            assert False, "unhandled exception"
    
    #check for exiting file conflicts
    if os.path.isfile(file) and newfile:
        confirmation = input('File already exists, overwrite? [y/n]: ')
        if confirmation.lower() != 'y':
            print('Exiting.')
            sys.exit(0)
    elif not os.path.isfile(file) and not newfile:
        print('Locker file not found, exiting.')
        sys.exit(0)

    #prompt for new password
    while not len(password):
        password = getpassword(newfile)
    
    try:    
        run_locker(file, password, newfile)
    except ValueError:
        print('Password is incorrect, exiting.')

if __name__ == "__main__":    
    main()