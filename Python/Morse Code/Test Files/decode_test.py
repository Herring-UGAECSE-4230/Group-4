mc = {'a': '.- ','b': '-... ', 'c': '-.-. ','d': '-.. ','e': '. ',
    'f': '..-. ','g': '--. ','h': '.... ','i': '.. ','j': '.--- ','k': '-.- ',
    'l': '.-.. ','m': '-- ','n': '-. ','o': '--- ', 'p': '.--. ', 'q': '--.- ',
    'r': '.-. ','s': '... ','t': '- ', 'u': '..- ', 'v': '...- ', 'w': '.-- ',
    'x': '-..- ', 'y': '-.-- ', 'z': '--.. ',
    '0': '----- ','1': '.---- ','2': '..--- ','3': '...-- ','4': '....- ',
    '5': '..... ','6': '-.... ','7': '--... ','8': '---.. ','9': '----. ', 'attention':'-.-.- ', 'over': '-.- ', 'out':'-.-. '    }

mc_decode = {v : k for k,v in mc.items()}
# ['...-.-.-.-.-']
# ['...-.-.-.-.- ']

with open('messages.txt', 'w') as file:
    word = '.- ... ... bruh '
    word = '...-. -.- .-.-'
    file.write(word)
    file.write(' | ')
    word = word.split()
    print(word)
    word = [word + ' ' for word in word]
    print(word)
    decode = [mc_decode.get(word, '?') for word in word]
    for n in decode:
        file.write(n)
    file.write(' \n')
file.close()
        #
    #for n in word:
   #     print(word[n])
    
   
#     file.write(decoded + '\n')
