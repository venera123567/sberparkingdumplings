def removeAllWhitespaces(str):
    return str.replace(' ', '')

def transformToEnKeys(str):
    dict = {'А': 'A',
    'В': 'B',
    'Е': 'E',
    'К': 'K',
    'М': 'M',
    'Н': 'H',
    'О': 'O',
    'С': 'C',
    'Т': 'T',
    'У': 'Y',
    'Х': 'X'}
    letters = list(str)
    newLetters = list(map(lambda letter: dict[letter] if letter in dict else letter, letters))
    return ''.join(newLetters)

def transformCarNumber(str):
    strUpper = str.upper()
    return transformToEnKeys(removeAllWhitespaces(strUpper))
