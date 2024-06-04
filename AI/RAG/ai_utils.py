
def convert_text_file_to_utf8(file_name):
    
    with open(file_name, "r") as file:
        unencoded_file = file.read()

    with open(file_name + "1", "w", encoding="UTF-8") as new_file:
        new_file.write(unencoded_file)
        
    return new_file

a = "qtwer"
ab = list(a)
def hi(*c):
    print(list(c))

hi(*ab)