# From https://gist.github.com/ebuckley/1842461
# 
# added: numbers and = symbol
# 
# Note, there's a bug where if the final morse symbol ends at the end
# of the input string the function will fail. Workaround add an extra space...
#

morseAlphabet ={
        "A" : ".-",
        "B" : "-...",
        "C" : "-.-.",
        "D" : "-..",
        "E" : ".",
        "F" : "..-.",
        "G" : "--.",
        "H" : "....",
        "I" : "..",
        "J" : ".---",
        "K" : "-.-",
        "L" : ".-..",
        "M" : "--",
        "N" : "-.",
        "O" : "---",
        "P" : ".--.",
        "Q" : "--.-",
        "R" : ".-.",
        "S" : "...",
        "T" : "-",
        "U" : "..-",
        "V" : "...-",
        "W" : ".--",
        "X" : "-..-",
        "Y" : "-.--",
        "Z" : "--..",
        "1" : ".----",
        "2" : "..---",
        "3" : "...--",
        "4" : "....-",
        "5" : ".....",
        "6" : "-....",
        "7" : "--...",
        "8" : "---..",
        "9" : "----.",
        "0" : "-----",
        " " : "/",
	"=" : "-...-"
        }

inverseMorseAlphabet=dict((v,k) for (k,v) in morseAlphabet.items())

# parse a morse code string positionInString is the starting point for decoding
def decodeMorse(code, positionInString = 0):
        
        if positionInString < len(code):
            morseLetter = ""
            for key,char in enumerate(code[positionInString:]):
                if char == " ":
                    positionInString = key + positionInString + 1
                    letter = inverseMorseAlphabet[morseLetter]
                    return letter + decodeMorse(code, positionInString)
                
                else:
                    morseLetter += char
        else:
            return ""
