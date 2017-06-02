def __stringToInt(number):
    for c in number:
        if(not (c >= '0' and c <= '9')):
            print('input error, expected only integer values')
            return None
    return int(number)
    

def getInteger(Q):
    number = input(Q + ': ').strip()
    for c in number:
        if(not (c >= '0' and c <= '9')):
            print('input error: ' + Q + ' can only be integer values')
            return None
    return int(number)

# gets an ISBN from the user. If there are any errors then it prints them and returns None
def getISBN(Q):
    ISBN = getInteger(Q)
    if(not ISBN): return None
    if(len(str(ISBN)) != 13):
        print(Q + ' requires exactly 13 digits')
        return None
    return ISBN


def __validateNotNullString(name, Q):
    if(len(name) == 0):
        print(Q + 'cannot be a null string')
        return None
    return name


def getNotNullName(Q):
    name = input(Q + ': ').strip()
    return __validateNotNullString(name, Q)


def getReadingDifficulty(Q):
    diff = __validateNotNullString(input(Q + ': ').strip(), Q)
    if(not diff): return None
    if(diff == 'Easy' or diff == 'Medium' or diff == 'Hard' or diff == 'Kids'):
        return diff
    print('error: unkown reading difficulty type \'' + diff + '\'. Expected one of \'Easy\', \'Medium\', \'Hard\', \'Kids\'')
    return None

# expects an input of space separated integers
def getIntegerList(Q):
    authorList = [__stringToInt(x) for x in input(Q + ': ').strip().split()]
    for a in authorList:
        if(a == None):
            return None
    return authorList

def getPrice(Q):
    number = input(Q + ': ').strip()
    for c in number:
        if(not ((c >= '0' and c <= '9') or c == '.')):
            print('input error: ' + Q + ' can only be numeric values')
            return None
    if(number.count('.') > 1):
        print('input error: ' + Q + ' can only be numeric values(found multiple decimals)')
    return float(number)

def getCondition(Q):
    cond = __validateNotNullString(input(Q + ': ').strip(), Q)
    if(not cond): return None
    if(cond == 'New' or cond == 'Like_New' or cond == 'Good' or cond == 'Ok' or cond == 'Bad'):
        return cond
    print('error: unkown condition type \'' + diff + '\'. Expected one of \'New\', \'Like_New\', \'Good\', \'Ok\', \'Bad\'')
    return None

def getFullName(Q):
    fullName = __validateNotNullString(input(Q + ': ').strip(), Q).split()
    fullName = [x for x in fullName if x] # remove empty strings
    if(len(fullName) != 2):
        print('error: full name expected (in the form of \'first_name last_name\')')
        return None
    return [x.strip() for x in fullName]

def getRating(Q):
    rating = getInteger(Q)
    if(rating < 0 or rating > 5):
        print('rating must be in the range [0, 5]')
        return None
    return rating




