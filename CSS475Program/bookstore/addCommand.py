import sqlite3
import parse
import random

def __addBook(cursor):
    ISBN = parse.getISBN('ISBN')
    if(ISBN == None): return

    name = parse.getNotNullName('book name')
    if(name == None): return

    genre = parse.getNotNullName('genre')
    if(genre == None): return

    publisher_id = parse.getInteger('publisher')
    if(publisher_id == None): return

    difficulty = parse.getReadingDifficulty('reading difficulty')
    if(difficulty == None): return

    # null preview content allowed
    preview_content = input('preview content(can be empty): ').strip()
    if(preview_content == ''): preview_content = None

    # get authors
    author_ids = parse.getIntegerList('author list(space separated integer ids)')
    if(author_ids == None): return

    cursor.execute("INSERT INTO BOOK VALUES(?, ?, ?, ?, ?, ?);", (ISBN, name, genre, publisher_id, difficulty, preview_content))

    for author in author_ids:
        cursor.execute("INSERT INTO AUTHORED_BY VALUES(?, ?);", (author, ISBN))



def __addBookInstance(cursor):
    book_id = 0

    # keep going until the random number does not collide
    while(True):
        book_id = random.randint(0, 1000000000)
        cursor.execute('SELECT Instance_id FROM BOOK_INSTANCE WHERE Instance_id = ?;', (book_id,))
        if(cursor.fetchone() == None): break
    
    ISBN = parse.getISBN('ISBN')
    if(ISBN == None): return

    price = parse.getPrice('price')
    if(price == None): return

    condition = parse.getCondition('condition')
    if(condition == None): return

    location = parse.getNotNullName('location in store(e.g. \'Isle 5\')')
    if(location == None): return

    store_id = parse.getInteger('store id')
    if(store_id == None): return

    cursor.execute("INSERT INTO BOOK_INSTANCE VALUES(?, ?, ?, ?, ?, ?, NULL, NULL);", (book_id, ISBN, price, condition, location, store_id))

def __addCustomer(cursor):
    customer_id = 0

    # keep going until the random number does not collide
    while(True):
        customer_id = random.randint(0, 1000000000)
        cursor.execute('SELECT Customer_id FROM CUSTOMER WHERE Customer_id = ?;', (customer_id,))
        if(cursor.fetchone() == None): break
    
    fullName = parse.getFullName('full name(first_name last_name)')
    if(fullName == None): return
    
    email = parse.getNotNullName('email address')
    if(email == None): return
    
    phone = parse.getInteger('phone number(type 0 if none)')
    if(phone == None): return
    if(phone == 0): phone = None

    billing_address = parse.getNotNullName('billing address')
    if(billing_address == None): return

    shiping_address = input('shipping address(empty to be same as billing): ').strip()
    if(shiping_address == ''): shiping_address = None

    password = parse.getNotNullName('customer password')
    if(password == None): return

    cursor.execute("INSERT INTO CUSTOMER VALUES(?, ?, ?, ?, ?, ?, ?, ?);", (customer_id, fullName[0], fullName[1], email, phone, billing_address, shiping_address, password))

def __addStore(cursor):
    store_id = 0

    # keep going until the random number does not collide
    while(True):
        store_id = random.randint(0, 1000000000)
        cursor.execute('SELECT Store_id FROM STORE WHERE Store_id = ?;', (store_id,))
        if(cursor.fetchone() == None): break

    name = parse.getNotNullName('store name')
    if(name == None): return
    
    address = parse.getNotNullName('store address')
    if(address == None): return

    cursor.execute("INSERT INTO STORE VALUES(?, ?, ?);", (store_id, name, address))


def __addPublisher(cursor):
    publisher_id = 0

    # keep going until the random number does not collide
    while(True):
        publisher_id = random.randint(0, 1000000000)
        cursor.execute('SELECT Publisher_id FROM PUBLISHER WHERE Publisher_id = ?;', (publisher_id,))
        if(cursor.fetchone() == None): break

    name = parse.getNotNullName('publisher name')
    if(name == None): return
    
    address = parse.getNotNullName('publisher address')
    if(address == None): return

    phone = parse.getInteger('phone number(type 0 if none)')
    if(phone == None): return
    if(phone == 0): phone = None
    

    cursor.execute("INSERT INTO PUBLISHER VALUES(?, ?, ?, ?);", (publisher_id, address, phone, name))


def __addAuthor(cursor):
    author_id = 0

    # keep going until the random number does not collide
    while(True):
        publisher_id = random.randint(0, 1000000000)
        cursor.execute('SELECT author_id FROM AUTHOR WHERE author_id = ?;', (author_id,))
        if(cursor.fetchone() == None): break

    name = parse.getNotNullName('author name')
    if(name == None): return

    biography = parse.getNotNullName('biography')
    if(biography == None): return

    cursor.execute("INSERT INTO AUTHOR VALUES(?, ?, ?);", (author_id, name, biography))


def __addReview(cursor):
    customer_id = parse.getInteger('reviewer(customer id)')
    if(customer_id == None): return

    ISBN = parse.getISBN('ISBN getting reviewed')
    if(ISBN == None): return

    rating = parse.getRating('rating(range [0, 5])')
    if(rating == None): return

    content = parse.getNotNullName('review content')
    if(content == None): return


    cursor.execute("INSERT INTO REVIEW VALUES(?, ?, ?, ?);", (content, rating, ISBN, customer_id))

    



# handle add command by delegating to one of the help functions above
def addCommand(args, connection):
    if(len(args) < 2):
        print(args[0] + ' requires one parameter (see \'help add\')')
        return
    type = args[1]

    c = connection.cursor()
    if(type == 'book'):
        if(len(args) > 2 and args[2] == 'instance'):
            __addBookInstance(c)
        else:
            __addBook(c)
    elif(type == 'customer'):
        __addCustomer(c)
    elif(type == 'store'):
        __addStore(c)
    elif(type == 'publisher'):
        __addPublisher(c)
    elif(type == 'author'):
        __addAuthor(c)
    elif(type == 'review'):
        __addReview(c)
    else:
        print('cannot add a \'' + type + '\' because that type is not known. For help type \'help add\'')
        return # prevent worthless commit

    connection.commit()
        
