def __stringToInt(number, required=True):
    for c in number:
        if(not (c >= '0' and c <= '9')):
            if(required):
                print('input error, expected only integer values')
            return None
    return int(number)


def getInteger(Q, required=True):
    number = input(Q + ': ').strip()
    if(not number): return None
    for c in number:
        if(not (c >= '0' and c <= '9')):
            if(required):
                print('input error: ' + Q + ' can only be integer values')
            return None
    return int(number)

# gets an ISBN from the user. If there are any errors then it prints them and returns None
def getISBN(Q, required=True):
    ISBN = getInteger(Q, required)
    if(not ISBN): return None
    if(len(str(ISBN)) != 13):
        if(required):
            print(Q + ' requires exactly 13 digits')
        return None
    return ISBN


def __validateNotNullString(name, Q, required=True):
    if(len(name) == 0):
        if(required):
            print(Q + 'cannot be a null string')
        return None
    return name


def getNotNullName(Q, required=True):
    name = input(Q + ': ').strip()
    return __validateNotNullString(name, Q, required)


def getReadingDifficulty(Q, required=True):
    diff = __validateNotNullString(input(Q + ': ').strip(), Q, required)
    if(not diff): return None
    if(diff == 'Easy' or diff == 'Medium' or diff == 'Hard' or diff == 'Kids'):
        return diff
        if(required):
            print('error: unkown reading difficulty type \'' + diff + '\'. Expected one of \'Easy\', \'Medium\', \'Hard\', \'Kids\'')
    return None

# expects an input of space separated integers
def getIntegerList(Q, required=True):
    authorList = [__stringToInt(x, required) for x in input(Q + ': ').strip().split()]
    for a in authorList:
        if(a == None):
            return None
    return authorList

def getPrice(Q, required=True):
    number = input(Q + ': ').strip()
    if(not number): return None
    for c in number:
        if(not ((c >= '0' and c <= '9') or c == '.')):
            if(required):
                print('input error: ' + Q + ' can only be numeric values')
            return None
    if(number.count('.') > 1):
        if(required):
            print('input error: ' + Q + ' can only be numeric values(found multiple decimals)')
    return float(number)

def getCondition(Q, required=True):
    cond = __validateNotNullString(input(Q + ': ').strip(), Q, required)
    if(not cond): return None
    if(cond == 'New' or cond == 'Like_New' or cond == 'Good' or cond == 'Ok' or cond == 'Bad'):
        return cond
        if(required):
            print('error: unkown condition type \'' + diff + '\'. Expected one of \'New\', \'Like_New\', \'Good\', \'Ok\', \'Bad\'')
    return None

def getFullName(Q, required=True):
    fullName = __validateNotNullString(input(Q + ': ').strip(), Q, required)
    if(not fullName): return None
    fullName = [x for x in fullName.split() if x] # remove empty strings
    if(len(fullName) != 2):
        if(required):
            print('error: full name expected (in the form of \'first_name last_name\')')
        return None
    return [x.strip() for x in fullName]

def getRating(Q, required=True):
    rating = getInteger(Q, required)
    if(rating < 0 or rating > 5):
        if(required):
            print('rating must be in the range [0, 5]')
        return None
    return rating
