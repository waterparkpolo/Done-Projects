import random
import sys

def main():
    gl=get_level()
    generate_integer(gl)
    print(f"Score:{score}")
    sys.exit()
def get_level():
    while True:
        try:
            lvl=int(input("Level: "))
            if lvl < 1:
                pass
            elif lvl > 3:
                pass
            elif lvl > 0:
                break
            else:
                pass
        except ValueError:
            pass
    return lvl


def generate_integer(level):
    global score
    score=0
    equation=0
    if level==1:
        while True:
            a= random.randint(0,9)
            b= random.randint(0,9)
            print(f'{a} + {b} = ', end='')
            AB=a+b
            user_answer=int(input())
            if user_answer == AB:
                score+=1
            if user_answer != AB:
                print("EEE")
                print(f'{a} + {b} = ', end='')
                user_answer1=int(input())
                if user_answer1 == AB:
                    score+=0
                if user_answer1 != AB:
                    print("EEE")
                    print(f'{a} + {b} = ', end='')
                    user_answer11=int(input())
                    if user_answer11 == AB:
                        score+=0
                    if user_answer11 != AB:

                        print("EEE")
                        print(f'{a} + {b} = {AB}')
            equation+=1
            if equation>9:
                break
    if level==2:
        while True:
            a= random.randint(10,99)
            b= random.randint(10,99)
            print(f'{a} + {b} = ', end='')
            AB=a+b
            user_answer=int(input())
            if user_answer == AB:
                score+=1
            if user_answer != AB:
                print("EEE")
                print(f'{a} + {b} = ', end='')
                user_answer1=int(input())
                if user_answer1 == AB:
                    score+=0
                if user_answer1 != AB:
                    print("EEE")
                    print(f'{a} + {b} = ', end='')
                    user_answer11=int(input())
                    if user_answer11 == AB:
                        score+=0
                    if user_answer11 != AB:

                        print("EEE")
                        print(f'{a} + {b} = {AB}')
            equation+=1
            if equation>9:
                break
    if level==3:
        while True:
            a= random.randint(100,999)
            b= random.randint(100,999)
            print(f'{a} + {b} = ', end='')
            AB=a+b
            user_answer=int(input())
            if user_answer == AB:
                score+=1
            if user_answer != AB:
                print("EEE")
                print(f'{a} + {b} = ', end='')
                user_answer1=int(input())
                if user_answer1 == AB:
                    score+=0
                if user_answer1 != AB:
                    print("EEE")
                    print(f'{a} + {b} = ', end='')
                    user_answer11=int(input())
                    if user_answer11 == AB:
                        score+=0
                    if user_answer11 != AB:

                        print("EEE")
                        print(f'{a} + {b} = {AB}')
            equation+=1
            if equation>9:
                break









if __name__ == "__main__":
    main()
