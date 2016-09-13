import sys
import getopt
import getpass

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
    
#def run_locker(filename, password, newfile):   

def main():

    if len(sys.argv[1:]) < 2:
        usage()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:f:p:",
        ["help", "new", "file","password"])
    except getopt.Getopterror as err:
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
        
    #run_locker(file, password, newfile)

if __name__ == "__main__":    
    main()