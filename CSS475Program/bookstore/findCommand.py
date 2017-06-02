import sqlite3
import parse

def __findBooks(cursor):
	print('every one of the following are optional. If you leave them all empty, then all books will be returned')

	ISBN = parse.getISBN('ISBN', False)
	name = parse.getNotNullName('book name', False)
	genre = parse.getNotNullName('genre', False)
	publisher_id = parse.getInteger('publisher id', False)
	difficulty = parse.getReadingDifficulty('reading difficulty', False)
	#unsure of how to handle author_ids
	#author_ids = parse.getIntegerList('author list(space separated integer ids)', False)
	store_id = parse.getInteger('store_id', False)
	min_price = parse.getPrice('minimum price', False)
	max_price = parse.getPrice('maximum price', False)
	condition = parse.getCondition('condition', False)

	where_clause = ""
	def addCond(total, cond):
		if(not total):
			return " WHERE " + cond
		else:
			return total + " AND " + cond

	def stringify(x):
		if(not x): return ''
		elif(x[0] == '\''): return x
		return '\'' + x + '\''

	# note: not safe against SQL injections!
	if(ISBN):
		where_clause = addCond(where_clause, "Book.ISBN = " + str(ISBN))
	if(name):
		where_clause = addCond(where_clause, "Name = " + stringify(name))
	if(genre):
		where_clause = addCond(where_clause, "Genre = " + stringify(genre))
	if(publisher_id):
		where_clause = addCond(where_clause, "publisher_id = " + str(publisher_id))
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

	query = "SELECT BOOK.ISBN, Instance_id, Price, Condition, store_id FROM BOOK" +\
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
    if(type == 'books'):
        __findBooks(c)
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
