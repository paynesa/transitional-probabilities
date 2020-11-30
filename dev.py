def remove_word_boundaries(input : str)->str:
    output = ""
    for char in input:
        if char != 'W':
            output += char
    return output



input : str = ""
for line in open("mother.speech.txt"):
    input += line.strip()

print(input[1:20])
print(remove_word_boundaries(input)[1:20])
