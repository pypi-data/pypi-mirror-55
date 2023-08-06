def add(param1, param2):
    return (param1+param2)

def centuryFromYear(year):
    x=year/100
    y=year%100
    if y==0:
        return int(x)
    else:
        return int(x)+1
centuryFromYear(1900)

def checkPalindrome(inputstring):
    return inputstring==inputstring[::-1]

def adjacentElementsProduct(input):
    a=input[0]
    produ=a*input[1]
    for i in input[1:]:
        if a*i>produ:
              produ=a*i
        a=i
    return produ


def shapeArea(n):
    n = (n**2)+((n-1)**2)
    return n
n = shapeArea(2)
