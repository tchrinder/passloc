import sys
import getopt
import getpass
import lockercrypto

def usage():
    print('''passloc - password management tool
        
        Usage: passloc.py -n filename -p password
               passloc.py -f filename -p password
        -n --new - create a new passloc file
        -f --file - access existing passloc file
        -p --password - password for passloc file, optional
        
        ''')
    sys.exit(0)

def getpassword(confirm):
    password = getpass.getpass()
    if confirm:
        if password != getpass.getpass('Confirm password: '):
            print('Passwords don\'t match, try again.')
            return ''
    return password

def select_service(pd):
    print('')
    service = input('Enter a service (ie gmail, amazon, netflix): ')
    try:
        print('{: >15} {: >15} {: >15}'.format('Service','Username','Password'))
        print(''.ljust(50,'-'))
        result = '{: >15} {: >15} {: >15}'.format(
            service,pd[service].split(':')[0],pd[service].split(':')[1])
        print(result)
        print('')
    except KeyError:
        print('SERVICE NOT FOUND')
        print('')
    
def select_all(pd):
    print('')
    print('{: >15} {: >15} {: >15}'.format('Service','Username','Password'))
    print(''.ljust(50,'-'))
    for key,value in pd.items():
        print('{: >15} {: >15} {: >15}'.format(
            key,value.split(':')[0],value.split(':')[1]))
    print('')

def delete_service(pd):
    service = input('Enter a service (ie gmail, amazon, netflix): ')
    try:
        del pd[service]
    except KeyError:
        print('SERVICE NOT FOUND')
        print('')
        return
    print(service + ' credentials deleted')
    print('')

def delete_all(pd):
    confirmation = input('Are you sure you want to delete all credentials? [y/n]: ')
    if confirmation.lower() == 'y':
        pd.clear()
        print('Locker cleared')
    else:
        print('Deletion aborted')
    print('')
    
def add_service(pd):
    print('')
    service = input('Enter a service (ie gmail, amazon, netflix): ')
    username = input('Enter service username: ')
    password = input('Enter service password: ')
    pd[service] = username + ':' + password
    print('')
    
def run_locker(filename, password, newfile):
    if not newfile:
        password_dictionary = lockercrypto.decrypt(filename, password)
    else:
        password_dictionary = {}
    
    print('Password Locker initialization successful')
    print('')
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

    if len(sys.argv[1:]) < 2:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:f:p:",
        ["help", "new", "file","password"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        
    password = ''
    file = ''
    newfile = False
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

    while not len(password):
        password = getpassword(newfile)
    
    try:    
        run_locker(file, password, newfile)
    except FileNotFoundError:
        print('Locker file not found, exiting.')
    except ValueError:
        print('Password is incorrect, exiting.')

if __name__ == "__main__":    
    main()