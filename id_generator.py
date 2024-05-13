from random import choice
#I know, this is a bit of trolling, but works :)
letters = ["A","B","C","D","E",
           "F","G","H","I","J",
           "K","L","M","N","O",
           "P","Q","R","S","T",
           "U","V","X","Y","Z"]
numbers = ["0","1","2","3","4",
           "5","6","7","8","9"]
def generate_id():
    id = ""
    id += choice(numbers)
    id += choice(numbers)
    id += choice(letters)
    id += choice(letters)
    id += choice(letters)
    id += choice(letters)
    id += choice(letters)
    id += choice(letters)
    return id
