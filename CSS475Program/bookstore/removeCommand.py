import sqlite3
import parse

def __removeBook(cursor):
    instance_id = parse.getInteger('book instance id')
    if(instance_id == None): return
    
    cursor.execute('DELETE FROM BOOK_INSTANCE WHERE instance_id = ?;', (instance_id,))
    
    if(cursor.rowcount == 0):
        print('book with inputed instance could not be found(and thus could not be deleted)')
    else:
        print('succesfully deleted book instance from the system')
    
    
def __removeStore(cursor):
    pass
    
    
def __removeReview(cursor):
    pass
    

def removeCommand(args, connection):
    if(len(args) < 2):
        print(args[0] + ' requires one parameter (see \'help remove\')')
        return
    type = args[1]

    c = connection.cursor()
    if(type == 'book'):
        if(len(args) > 2 and args[2] == 'instance'):
            __removeBook(c)
        else:
            print('can only remove book instance')
            return # prevent worthless commit
    elif(type == 'store'):
        __removeStore(c)
    elif(type == 'review'):
        __removeReview(c)
    else:
        print('cannot rmove a \'' + type + '\' because that type is not known. For help type \'help remove\'')
        return # prevent worthless commit

    connection.commit()
