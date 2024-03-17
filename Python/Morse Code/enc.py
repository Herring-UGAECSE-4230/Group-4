with open('input.txt') as file:
    lines = [line.rstrip() for line in file.readlines()]


mc = {
    'a': '.- ',
    'b': '-... ',
    'c': '-.-. ',
    'd': '-.. ',
    'e': '. ',
    'f': '..-. ',
    'g': '--. ',
    'h': '.... ',
    'i': '.. ',
    'j': '.--- ',
    'k': '-.- ',
    'l': '.-.. ',
    'm': '-- ',
    'n': '-. ',
    'o': '--- ',
    'p': '.--. ',
    'q': '--.- ',
    'r': '.-. ',
    's': '... ',
    't': '- ',
    'u': '..- ',
    'v': '...- ',
    'w': '.-- ',
    'x': '-..- ',
    'y': '-.-- ',
    'z': '--.. '    
    }

def translate(char):
    if char not in mc:
        return ' '
    return mc[char]

def mcword(word):
    if word == 'attention':
        return '-.-.-'
    if word == 'over':
        return '-.-'
    if word == 'out':
        return '.-.-.'
    return ''.join([translate(i) for i in word])

# print(mcword('attention') + '| ' + 'attention') 
# for line in lines:
#     line = line.split(' ')
#     for i in range(len(line)):
#         if i == 0:
#             print(mcword(line[i]) + '| ' + line[i])
#         else:
#             print('       ' + mcword(line[i]) + '| ' + line[i])
#     print(mcword('over') + '| ' + 'over')
# print(mcword('out') + '| ' + 'out')
f = open('output.txt', 'w')
f.write(mcword('attention') + '| ' + 'attention' + '\n') 
for line in lines:
    line = line.split(' ')
    for i in range(len(line)):
        if i == 0:
            f.write(mcword(line[i]) + '| ' + line[i] + '\n')
        else:
            f.write('       ' + mcword(line[i]) + '| ' + line[i] + '\n')
    f.write(mcword('over') + '| ' + 'over' + '\n')
f.write(mcword('out') + '| ' + 'out' + '\n')
f.close()