import sqlite3

def __findBookInstance(cursor):
	pass

def __findBook(cursor):
	pass

def __findCustomer(cursor):
	pass

def __findStore(cursor):
	pass

def __findPublisher(cursor):
	pass

def __findAuthor(cursor):
	pass

def __findReview(cursor):
	pass


def findCommand(args, connection):
    if(len(args) < 2):
        print(args[0] + ' requires one parameter (see \'help find\')')
        return
    type = args[1]

    c = connection.cursor()
    if(type == 'book'):
        if(len(args) > 2 and args[2] == 'instance'):
            __findBookInstance(c)
        else:
            __findBook(c)
    elif(type == 'customer'):
        __findCustomer(c)
    elif(type == 'store'):
        __findStore(c)
    elif(type == 'publisher'):
        __findPublisher(c)
    elif(type == 'author'):
        __findAuthor(c)
    elif(type == 'review'):
        __findReview(c)
    else:
        print('cannot find a \'' + type + '\' because that type is not known. For help type \'help find\'')
        return # prevent worthless commit

    connection.commit()
