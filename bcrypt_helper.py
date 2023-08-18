import bcrypt
import getpass


def promptUser(usr_file):
    status = False
    while not status:
        usr = input("Username? ").upper()
        usrInfo = checkUser(usr, usr_file)
        if(usrInfo is not False):
            pwd = getpass.getpass("Passsword? ").encode()
            pwdHashed = bcrypt.checkpw(pwd, usrInfo[1].encode())
            if pwdHashed:
                print("Welcome, " + usr.capitalize() + ". Have a nice day.")
                return usr
            else:
                print("Incorrect username or password. Please try again :(")
        else:
            createPrompt = input("user does not exist. Create user?")
            if createPrompt == 'y' or createPrompt == 'Y' or createPrompt == 'yes' or createPrompt == 'Yes':
                createUser(usr, usr_file)


def createUser(usr, usr_file):
    confirm = False
    while not confirm:
        pwd = getpass.getpass("Choose a password: ").encode()
        pwdConfirm = getpass.getpass("Confirm password: ").encode()
        if pwd == pwdConfirm:
            confirm = True
        else:
            print("Passwords do not match! Please try again.")
    passHash = bcrypt.hashpw(pwd, bcrypt.gensalt())
    str(passHash)
    line = usr + " " + passHash.decode()
    usr_file.write("%s\n" % line)
    print("User created. Please login with your credentials.")
    usr_file.seek(0)


def checkUser(usr, usr_file):
    usr_file.seek(0)
    for line in usr_file:
        values = line.split()
        if (values[0] == usr):
            return values
    return False
