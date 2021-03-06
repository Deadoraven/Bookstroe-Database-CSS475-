import sqlite3
import parse

# helper to build sql commands.
# NOT injection safe!!!!!!
def addCond(total, cond):
	if(not total):
		return " WHERE " + cond
	else:
		return total + " AND " + cond

# adds single quotation marks around a string if it doesn't have then already
def stringify(x):
	if(not x): return ''
	elif(x[0] == '\''): return x
	return '\'' + x + '\''

def __findBooks(cursor):
	print('every one of the following are optional. If you leave them all empty, then all books will be returned')

	ISBN = parse.getISBN('ISBN', False)
	name = parse.getNotNullName('book name', False)
	genre = parse.getNotNullName('genre', False)
	Publisher_id = parse.getInteger('Publisher id', False)
	difficulty = parse.getReadingDifficulty('reading difficulty', False)
	#unsure of how to handle author_ids
	#author_ids = parse.getIntegerList('author list(space separated integer ids)', False)
	store_id = parse.getInteger('store_id', False)
	min_price = parse.getPrice('minimum price', False)
	max_price = parse.getPrice('maximum price', False)
	condition = parse.getCondition('condition', False)

	where_clause = ""

	# note: not safe against SQL injections!
	if(ISBN):
		where_clause = addCond(where_clause, "Book.ISBN = " + str(ISBN))
	if(name):
		where_clause = addCond(where_clause, "Name = " + stringify(name))
	if(genre):
		where_clause = addCond(where_clause, "Genre = " + stringify(genre))
	if(Publisher_id):
		where_clause = addCond(where_clause, "Publisher_id = " + str(Publisher_id))
	if(difficulty):
		where_clause = addCond(where_clause, "Reading_difficulty = " + stringify(difficulty))

	if(store_id):
		where_clause = addCond(where_clause, "store_id = " + str(store_id))
	if(min_price):
		where_clause = addCond(where_clause, "price >= " + str(min_price))
	if(max_price):
		where_clause = addCond(where_clause, "price <= " + str(max_price))
	if(condition):
		where_clause = addCond(where_clause, "condition = " + stringify(condition))

	query = "SELECT BOOK.ISBN, Instance_id, Price, Condition, store_id, BOOK.name FROM BOOK" +\
		" INNER JOIN BOOK_INSTANCE ON BOOK.ISBN = BOOK_INSTANCE.ISBN" +\
		where_clause + ";"

	# debug info
	# print('running query: ' + query)

	cursor.execute(query)

	print('')
	print('')
	print('')
	print('search results:')
	matches = cursor.fetchall()
	for match in matches:
		print('ISBN: ' + str(match[0]))
		print('name: ' + str(match[5]))
		print('instance_id: ' + str(match[1]))
		print('Price: ' + str(match[2]))
		print('Condition: ' + match[3])

		cursor.execute("SELECT * FROM STORE WHERE Store_id = ?;", (match[4], ))
		m = cursor.fetchone()
		print('Store/Warehouse Id: ' + str(m[0]))
		print('Store/Warehouse Name: ' + str(m[1]))
		print('Store/Warehouse Address: ' + str(m[2]))
		print('') # empty line


def __findCustomer(cursor):
	print('every one of the following are optional. If you leave them all empty, then all customers will be returned')
	customer_id = parse.getInteger('customer id', False)
	name = parse.getFullName('full name(first_name last_name)', False)
	email = parse.getNotNullName('email address', False)

	where_clause = ""

	# note: not safe against SQL injections!
	if(customer_id):
		where_clause = addCond(where_clause, "customer_id = " + str(customer_id))
	if(name):
		where_clause = addCond(where_clause, "FName = " + stringify(name[0]))
		where_clause = addCond(where_clause, "LName = " + stringify(name[1]))
	if(email):
		where_clause = addCond(where_clause, "email_address = " + stringify(email))

	cursor.execute("SELECT * FROM CUSTOMER" + where_clause + ";")
	print('')
	print('')
	print('')
	print('search results:')
	matches = cursor.fetchall()
	for match in matches:
		print('customer_id: ' + str(match[0]))
		print('Name: ' + str(match[1]) + ' ' + str(match[2]))
		print('email address: ' + str(match[3]))
		print('phone number: ' + str(match[4]))
		print('billing address: ' + str(match[5]))
		shipping = match[6] or str(match[5]) # defaults to billing if no shipping specified
		print('shipping address: ' + shipping)
		print('*really secure password: ' + str(match[7]))

		# get cart
		cursor.execute("SELECT Instance_id, Price, Condition, BOOK.ISBN, BOOK.name FROM \
			BOOK_INSTANCE INNER JOIN BOOK ON BOOK_INSTANCE.ISBN = BOOK.ISBN WHERE BOOK_INSTANCE.Customer_id = ?;", (match[0], ))
		books = cursor.fetchall()
		print('')
		print('current cart:')
		for book in books:
			print('book Instance_id: ' + str(book[0]))
			print('book title: ' + str(book[4]))
			print('book Price: ' + str(book[1]))
			print('book Condition: ' + str(book[2]))
			print('book ISBN: ' + str(book[3]))
			print('')


		# get past orders
		print('list of previous orders:')
		cursor.execute("SELECT Order_id, Billing_address, Shipping_address, Order_date FROM \
			BOOK_ORDER WHERE Customer_id = ?;", (match[0], ))
		orders = cursor.fetchall()
		for order in orders:
			print('order id: ' + str(order[0]))
			print('order billing address: ' + str(order[1]))
			print('order shipping address: ' + str(order[2]))
			print('order date: ' + str(order[3]))
			print('list of book instance ids, ISBNs, and names:')
			cursor.execute("SELECT Instance_id, BOOK.ISBN, BOOK.name FROM \
				BOOK INNER JOIN BOOK_INSTANCE ON BOOK.ISBN = BOOK_INSTANCE.ISBN WHERE Order_id = ?;", (order[0], ))
			books = cursor.fetchall()
			for book in books:
				print(str(book[0]) + ' ' + str(book[1]) + ' ' + str(book[2]))

			print('')
		print('')
	print('')
	print('')
	print('* okay, the password isn\'t really secure... at all')

def __findPublisher(cursor):

	print('every one of the following are optional. If you leave them all empty, then all customers will be returned')
	publisher_id = parse.getInteger('Publisher id', False)
	name = parse.getNotNullName('Publisher\'s name', False)
	address = parse.getNotNullName('Publisher\'s address', False)
	phone = parse.getInteger('Publisher\'s phone number' ,False)

	where_clause = ""
	# note: not safe against SQL injections!
	if(publisher_id):
		where_clause = addCond(where_clause, "publisher_id = " + str(publisher_id))
	if(name):
		where_clause = addCond(where_clause, "name = " + stringify(name))
	if(address):
		where_clause = addCond(where_clause, "address = " + stringify(address))
	if(phone):
		where_clause = addCond(where_clause, "phone = " + str(phone))


	cursor.execute("SELECT * FROM PUBLISHER" + where_clause + ";")
	print('')
	print('')
	print('search results:')
	matches = cursor.fetchall()
	for match in matches:
		print('Publisher id: ' + str(match[0]))
		print('Publisher\'s name: ' + str(match[3]))
		print('Publisher\'s address: ' + str(match[2]))
		print('Publisher\'s phone number: ' + str(match[1]))
		print('')
	print('')

def __findAuthor(cursor):
	print('every one of the following are optional. If you leave them all empty, then all customers will be returned')
	author_id = parse.getInteger('Author\'s id', False)
	name = parse.getNotNullName('Author\'s name', False)
	biography = parse.getNotNullName('Author\'s address', False)

	where_clause = ""

	# note: not safe against SQL injections!
	if(author_id):
		where_clause = addCond(where_clause, "author_id = " + str(author_id))
	if(name):
		where_clause = addCond(where_clause, "name = " + stringify(name))
	if(biography):
		where_clause = addCond(where_clause, "biography= " + stringify(biography))

	cursor.execute("SELECT * FROM AUTHOR" + where_clause + ";")
	print('')
	print('')
	print('search results:')
	matches = cursor.fetchall()
	for match in matches:
		print('Author\'s id: ' + str(match[0]))
		print('Author\'s name: ' + str(match[1]))
		print('Author\'s biography: ' + str(match[2]))
		print('')
	print('')

def __findReview(cursor):
	print('every one of the following are optional. If you leave them all empty, then all reviews will be returned.')
	print('Reviews are sorted by reviewer. reviewer is the customer who wrote the review')
	customer_id = parse.getInteger('reviewer id', False)
	customer_name = parse.getFullName('reviewer full name(first_name last_name)', False)
	email = parse.getNotNullName('reviewer email address', False)

	ISBN = parse.getNotNullName('book ISBN', False)
	book_name = parse.getNotNullName('book title', False)

	where_clause = ""
	# note: not safe against SQL injections!
	if(customer_id):
		where_clause = addCond(where_clause, "C.customer_id = " + str(customer_id))
	if(customer_name):
		where_clause = addCond(where_clause, "C.FName = " + stringify(customer_name[0]))
		where_clause = addCond(where_clause, "C.LName = " + stringify(customer_name[1]))
	if(email):
		where_clause = addCond(where_clause, "C.email_address = " + stringify(email))

	if(ISBN):
		where_clause = addCond(where_clause, "B.ISBN = " + str(ISBN))
	if(book_name):
		where_clause = addCond(where_clause, "B.Name = " + stringify(book_name))

	cursor.execute('SELECT C.customer_id, C.Fname, C.Lname, B.ISBN, B.name, R.Rating, R.content FROM \
		REVIEW AS R INNER JOIN CUSTOMER AS C ON R.customer_id = C.customer_id\
		INNER JOIN BOOK AS B ON R.ISBN = B.ISBN' + where_clause + ' ORDER BY R.customer_id;')

	print('')
	print('')
	print('')
	print('search results:')
	reviews = cursor.fetchall()
	for r in reviews:
		print('customer id: ' + str(r[0]))
		print('customer name: ' + str(r[1]) + ' ' + str(r[2]))
		print('book ISBN: ' + str(r[3]))
		print('book name: ' + str(r[4]))
		print('review content: ' + str(r[6]))
		print('review rating: ' + str(r[5]))
		print('')


def findCommand(args, connection):
    if(len(args) < 2):
        print(args[0] + ' requires one parameter (see \'help find\')')
        return
    type = args[1]

    c = connection.cursor()
    if(type == 'books'):
        __findBooks(c)
    elif(type == 'customers'):
        __findCustomer(c)
    elif(type == 'publisher'):
        __findPublisher(c)
    elif(type == 'store'):
        __findStore(c)
    elif(type == 'author'):
        __findAuthor(c)
    elif(type == 'reviews'):
        __findReview(c)
    else:
        print('cannot find a \'' + type + '\' because that type is not known. For help type \'help find\'')
        return # prevent worthless commit

    connection.commit()
