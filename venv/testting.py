'''

x, y = 0, 0

def en_funktion(x, y):
    x = 80
    y = 80
    return x, y

print (x, y) #printer 0, 0
en_funktion(x, y)
print(x, y) #printer også 0, 0

'''

class En_class:
    x = 80
    y = 80

instance_1 = En_class

print(En_class.x)
En_class.x = 40
print(En_class.x)