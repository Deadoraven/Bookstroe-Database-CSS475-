import sqlite3

# this dictionary is accessed by the help command. It requires a very strict structure where each entry looks like the example below:
# 'help_page_name' : {'summary' : 'give summary here', 'details' : 'provide details here'} note: summary and details need to be their names verbatim
help_dict = {
    'help' : {'summary': 'displays this help', 'details' :
        'if typed as just \'help\' prints a general summary of all commands. if typed as \'help command\' displays help specific to the command typed in.'},

    'add' : {'summary': 'adds an item of the type given as the first argument to the database with an interactive prompt', 'details' :
        '''adds an item of the type given as the first argument to the database with an interactive prompt. Specific things that can added: book, book instance, customer, store, publisher, author, review.
Make sure to have the necessary id\'s to run the command. See \'find\''''},

    'remove' : {'summary': 'removes something from the database given a key', 'details':
        '''add help'''},

    'find' : {'summary': 'finds the key of something from the database given details from an interactive prompt.', 'details':
        'finds the key of something from the database given details from an interactive prompt. Specific things that can found: books, customers, publishers, authors, reviews. \n\
    books: returns a list of book instances with useful information such as Price, Location, ISBN and name\n\
    customers: returns a list of customers with information such as customer id, name, their online cart and previous purchases\n\
    reviews: returns a list of reviews with information such as who wrote it, its content, the book it was for and the rating'},

    'sell' : {'summary': 'sells a book to a customer', 'details':
        'enters an interactive prompt which requires a customer id and book instance id. The system then moves the book to that customers ownership.'},

    'exit' : {'summary': 'exits the program', 'details':
        '''exits the program'''},

    'quit' : {'summary': 'exits the program', 'details':
        '''exits the program'''}
}

# returns a string with space padding it so the new stringg is the desired length. If str length is already equal or larger then this just returns the passed in string
def padString(str, length):
    diff = length - len(str)
    if(diff > 0):
        return str + ' ' * diff
    else:
        return str

# prints out generic help or help on a specific command if this is given an argument
def helpCommand(args, connection):
    if(len(args) > 1):
        try:
            help_string = help_dict[args[1]]
            print(help_string['details'])
        except KeyError:
            print('no help page for \'' + args[1] + '\'.')
    else:
        print('this is help from the bookstore application.')
        print('one note is that this application does not handle errors well right now. It will do one of two things:')
        print('    silently ignore the error(when you would like to know you typed a name into the number field!)')
        print('    report the error and exit(when you want to keep going!)')
        print('')
        print('below are a list of commands:')
        for key, value in help_dict.items():
            print(padString(key, 10) + ' : ' + value['summary'])
