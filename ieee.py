"""
2020 PyJaC coding competition.

PyJaC is a brand-new coding competition brought to you by UTM’s Women in Science
and Computing Club (WiSC), UTM Mathematical and Computational Sciences Society
(MCSS), and UTM Physics Club (PC).

Our prompt: creat an IEEE encoder/decoder

An IEEE encoder/decoder should convert floating-point numbers to a decimal
representation and back to floating-point, depending on the operation chosen.

Project completed by: Shaquille David
                      Junayeed Rahman
                      Mohid Sharif
"""
import math

###### ENCODING FUNCTIONS
# Part 1 - Represent the number as a binary number

def changeWholeToBin(number):
    """Change a whole number to its binary representation"""
        
    bits = []
        
    absnumber = abs(number)
    last_bit = absnumber%2
    bits.append(last_bit)

    quotient = absnumber//2

    while quotient != 0:
        bits.append(quotient%2)
        quotient = quotient//2

    if number < 0:
        bits.append('-')
        
    bits.reverse()
    
    return ''.join([str(elem) for elem in bits])

def changeDecimalToBin(decimal):
    """Return the first 20 bits of the decimal number to binary"""
    bits = []
    if decimal == 0:
        return ''
    i = 0
    while i < 20:
        product = decimal * 2
        bits.append(str(product)[0])
        decimal = float('0' + str(product)[1:])
        i = i + 1

    return ''.join([str(elem) for elem in bits])
    
        
def numToBinary(num):
    """Change a number to its binary representation
    >>> numToBinary(263.3)
    '100000111.01001100110011001100'
    """
    number_dec = num - int(num)
    number_whole = int(num)
    return changeWholeToBin(number_whole) + '.' + changeDecimalToBin(abs(number_dec))
    
# Part 2 - Change to scientific notation
def scientific(binarynum):
    """Change a binary number to its scientific notation equivalent

    >>> scientific('100000111.01001100110011001100')
    '1.0000011101001100110011001100e8'
    """
    
    bits = []
    for i in binarynum:
        bits.append(i)
        
    if bits[0] == '-':
        x = bits[1:]
        if '.' in bits:
            exponent = x.index(".") - 1
            x.remove(".")
            rest = ''.join(x[1:])
        elif '.' not in bits:
            exponent = len(x) - 1
            rest = ''.join(x[1:])
            
        return x[0] + '.' + rest + 'e' + str(exponent)
        
    else:
        if '.' in bits:
            exponent = bits.index(".") - 1 #DOUBLE CHECK THIS
            bits.remove(".")
            rest = ''.join(bits[1:])
        elif '.' not in bits:
            exponent = len(bits) - 1
            rest = ''.join(bits[1:])

        return bits[0] + '.' + rest + 'e' + str(exponent)


# Step 3 - [ENCODE] Write the scientific notation in IEEE-754 format
def encode(number):
    """Convert a decimal numbers to its IEEE-754 floating point representation

    >>> encode(263.3)
    '01000011100000111010011001100110'

    >>> encode(1020)
    '01000100011111110000000000000000'

    >>> encode(155.5)
    '01000011000110111000000000000000'
    
    >>> encode('inf')
    '01111111100000000000000000000000'

    >>> encode('wagwan popcaan')
    'Not a valid input'
    """
    
    if type(number) != int and type(number) != float:
        number = str(number)
        
    # special cases
    special = ['inf', '-inf', float(0), -float(0), 'NaN']
    
    if number in special:
        if number == float(0):
            return '00000000000000000000000000000000'
        elif number == -float(0):
            return '10000000000000000000000000000000'
        elif number == 'inf':
            return '01111111100000000000000000000000'
        elif number == '-inf':
            return '11111111100000000000000000000000'
        elif number == 'NaN':
            return '01111111111111111111111111111111'

    else:
        if type(number) == str:
            return 'Not a valid input'
        else:
            binaryrep = numToBinary(number)
            scientificrep = scientific(binaryrep)
            scientificrep = scientificrep.replace(".", '')
            bias = 127 #the exponential bias for a single precision number is 127
            indexofe = scientificrep.index('e')
            exponent = bias + int(scientificrep[indexofe + 1:])
            bits = []

            if number > 0:
                bits.append('0')
            elif number < 0:
                bits.append('1')

            exp_bits = changeWholeToBin(exponent)
            bits.append(exp_bits)

            i = 0
            while scientificrep[i+1] != 'e' and i < 23:
                bits.append(scientificrep[i+1])
                i = i + 1

            #last check
            if len(''.join(bits)) != 32:
                j = 32 - (len(''.join(bits)))
                while j != 0:
                    bits.append('0')
                    j = j - 1

            return ''.join(bits)



###### DECODING FUNCTIONS: Converting Floating-Point numbers to Decimal
# Part 1 - Find the Sign Bit

def getSignBit (sign):
    """
        The first bit is the Sign Bit

        0: Positive Decimal
        1: Negative Decimal
    """
    return int(sign.replace(' ', '')[:1])
    

def binaryToNum (binary):
    """
        convert Binary to Number
    """

    num = 0
    count = 0
    for i in range(len(binary) - 1, -1, -1):
        
        num += int(binary[i]) * (2 ** count)
        count += 1
    
    return num

def getExpBit (exp):
    """
        The 8 Bits after the first bit are the Exponent Bits
        Gives the value of the exponent of the decimal in Scientific Notation
        We convert Binary to Number by calling binaryToNum()
    """

    # removes spaces and sends the 8 Exponent Bits
    exponent = binaryToNum(exp.replace(' ', '')[1:9]) 

    # exp = exponent - 127
    # If exp > 0: Positive exponent
    #    exp < 0: Negative exponent
    
    return exponent

def mantissa (binary):
    """
        Finding the Mantissa from Float-Point
    """
    #print(len(binary[22]))
    num = 0
    count = -1
    for i in range(len(binary)):
        #print(str(i) + " " + str(binary[i]))
        num += int(binary[i]) * (2 ** count)
        count -= 1


    return num

def getFracBit (frac):
    """
        The remaining 23 Bits are the Mantissa
        Gives us the fraction value
        We find the fraction by calling mantissa()
    """

    #print(hexadecimal.replace(' ', '')[9:])
    fraction = mantissa(frac.replace(' ', '')[9:])
    return fraction

def ifBinary(binary):
    
    if len(binary) > 32:
        return False
    
    #Returns True/False for each number in binary matches '1' or '0' as a list
    binary_num = ['1', '0']
    matched = [num in binary_num for num in binary]
    return all(matched)
    

def floatToScientific (binary):
    """
        Writing the decimal in scientific notation using the
        Sign, Exponent, and Fraction
    """
    if ifBinary(binary):
        if len(binary) < 32:
           binary = ('0' * (32 - len(binary))) + binary
    
        #get sign bit
        sign = getSignBit(binary)
        fraction = getFracBit(binary)
        e = getExpBit(binary)
        if e == 0:
            e = -126
            return str(((-1)**sign) * (fraction)) + ' x ' + '2^' + str(e)
        else:
            e = e - 127
            return str(((-1)**sign) * (1 + fraction)) + ' x ' + '2^' + str(e)

        

    else:
        return 'Not Valid'

def floatToDecimal (binary):
    """
        Finding the actual decimal number using the
        Sign, Exponent, and Fraction
    """

    if ifBinary(binary):
        if len(binary) < 32:
            binary = ('0' * (32 - len(binary))) + binary

        sign = getSignBit(binary)
        e = getExpBit(binary)
        fraction = getFracBit(binary)
        if e == 0:
            e = -126
            return ((-1)**sign) * (fraction) * (2**e)
        else:
            e = e - 127
            return ((-1)**sign) * (1 + fraction) * (2**e)


    else:
        return 'Not valid'
    

if __name__ == '__main__':
    print(floatToDecimal('00000000000000000000000000000011'))
    
