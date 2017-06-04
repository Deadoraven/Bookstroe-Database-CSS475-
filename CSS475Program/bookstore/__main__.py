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

# when the command matching a key is typed it will call the function on the right with an array of parameters
# The parameter at index 0 is the name of the command itself (to support aliases)
command_dict = {
    'exit' : exitCommand,
    'quit' : exitCommand,
    'help' : helpCommand,
    'add' : addCommand,
    'sell' : sellCommand,
    'remove' : removeCommand,
    'find' : findCommand}

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
