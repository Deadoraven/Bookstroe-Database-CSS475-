from addCommand import addCommand
from helpCommand import helpCommand
from removeCommand import removeCommand
from findCommand import findCommand
from sellCommand import sellCommand
import sqlite3

# connection provides a way to access the database
connection = sqlite3.connect('bookstore.db')

# enable foreign key support
connection.cursor().execute("PRAGMA foreign_keys = 1")

exit = False
def exitCommand(args, connection):
    global exit
    exit = True

def QACommand(args, connection):
    print('this is a list of questions and answers')
    print('-------------------------------------------------------')
    print('Q: How do I add a book into the system?')
    print('A: Look at the \'add\' command. The answer to this question depends')
    print('   on what you mean by \'book\'. If you mean you want to add a book')
    print('   type to the system then type \'add book\' and enter information')
    print('   into the interactive prompt. If you mean a particular book instance')
    print('   then type \'add book instance\' and follow the interactive prompt')
    print('   note: book instances require a book type to refer to (by ISBN) which')
    print('   may have to be created first')
    print('')
    
    print('Q: how do I add a review?')
    print('A: simply type \'add review\' and follow the interactive prompt!')
    print('   note: you need to know the book ISBN and customer id')
    print('')
    
    print('Q: how do I sell a book directly?')
    print('A: simply type \'sell\' and follow the interactive prompt')
    print('')
    
    print('Q: how do I put a book in someones cart?')
    print('A: at this moment the UI has no access to the cart')
    print('')
    
    print('Q: how do I find XXX')
    print('A: type \'help find\' to learn how to use the find command')
    print('')

# when the command matching a key is typed it will call the function on the right with an array of parameters
# The parameter at index 0 is the name of the command itself (to support aliases)
command_dict = {
    'exit' : exitCommand,
    'quit' : exitCommand,
    'help' : helpCommand,
    'add' : addCommand,
    'sell' : sellCommand,
    'remove' : removeCommand,
    'find' : findCommand,
    'QA' : QACommand}

print('welcome to the bookstore application user interface!')
print('type \'help\' for help')
print('type \'QA\' for a list of questions and answers')

while(not exit):
    # get all words passed in by spliting at whitespaces and removing empty strings that result from double whitespaces
    words = [x for x in input('command: ').split() if x != '']

    # ignore empty commands
    if(len(words) == 0): continue
    command = words[0]


    try:
        command = command_dict[words[0]]
        command(words, connection)
    except KeyError:
        print('unkown command \'' + words[0] + '\'.')
