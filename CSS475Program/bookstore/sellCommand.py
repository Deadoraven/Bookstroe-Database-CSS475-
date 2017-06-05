import sqlite3
import parse
import random


def sellCommand(args, connection):
    customer_id = parse.getInteger('enter customer id')
    if(customer_id == None):
        return
    
    cursor = connection.cursor()
    cursor.execute('SELECT Fname, Lname, Billing_address, Shipping_address FROM CUSTOMER WHERE Customer_id = ?;', (customer_id, ))
    customer = cursor.fetchone()
    if(customer == None):
        print('unable to find customer with inputed id')
        return
    
    instance_id = parse.getInteger('enter book instance id')
    cursor.execute('SELECT instance_id, name, Order_id FROM BOOK_INSTANCE INNER JOIN BOOK ON BOOK_INSTANCE.ISBN = BOOK.ISBN WHERE instance_id = ?;', (instance_id, ))
    book = cursor.fetchone()
    if(book == None):
        print('unable to find book with inputed id')
        return
    if(book[2] != None):
        print('that book has already been sold!')
        return
    
    billing = parse.getNotNullName('billing address(optional)', False)
    shipping = parse.getNotNullName('shipping address(optional)', False)
    
    # prefers form up above then that of the customer(which is NOT NULL)
    billing = billing or str(customer[2])
    
    # prefers form up above, then that of the customer then that of billing
    shipping = shipping or customer[3] or billing
    
    order_id = 0
    # keep going until the random number does not collide
    # keeps random numbers as small as possible now
    max_r = 10
    while(True):
        order_id = random.randint(0, max_r)
        cursor.execute('SELECT Order_id FROM BOOK_ORDER WHERE Order_id = ?;', (order_id,))
        if(cursor.fetchone() == None): break
        max_r *= 10
    
    cursor.execute('INSERT INTO BOOK_ORDER VALUES(?, ?, ?, date(\'now\', \'localtime\'), ?);', (order_id, billing, shipping, customer_id))
    
    cursor.execute('UPDATE BOOK_INSTANCE SET Order_id = ? WHERE instance_id = ?;', (order_id, instance_id))
    print('succesfully sold the book \'' + book[1] + '\' to customer ' + str(customer[0]) + ' ' + str(customer[1]))
    connection.commit()
    