import random
import sys
def main():
    global x
    while True:
        try:
            x = int(input("What's your desired level?"))
            break
        except ValueError:
            pass
    if x < 1:
        main()
def game():
    global n
    n= random.randint(1, x)
    while True:
        try:
            g = int(input("Guess:"))
            if g < 1:
                pass
            elif g < n:
                print("Too small!")
            elif g > n:
                print("Too large!")
            elif g==n:
                sys.exit("Just Right!")
                break
        except ValueError:
            pass

main()
game()
