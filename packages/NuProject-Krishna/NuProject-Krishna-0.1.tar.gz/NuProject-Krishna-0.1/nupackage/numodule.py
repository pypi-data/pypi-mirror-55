import os, sys, string
    
def greet(name):
    print(f'Hello, {name}!')
    
def greet_main():
    if len(sys.argv) > 1:
        name = sys.argv[1]
    else:
        name = 'unknown human'
    greet(name)
