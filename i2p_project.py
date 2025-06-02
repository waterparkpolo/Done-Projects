def main():
    greet_user()
    get_identity()
    convert()


    if time_value>6.99 and time_value<8.01:
        print("breakfast time")

    elif time_value>11.99 and time_value<13.01:
        print("lunch time")

    elif time_value>17.99 and time_value<19.01:
        print("dinner time")
    else:
        print("It's not time to eat yet. Eating times are 7-8 a.m. for breakfast, 12-1 p.m. for lunch "
        "dinner time is 6-7 p.m.")

#7:00 tele eat, meal o matic, iEatery, tele meal, deal a meal, meal maniac, Feed me eatery, FastDeli
#Realworld meals, fill me meal me, QuikSup QuikEatz

def greet_user():
    print("Hello, this is QuikEatz. Who do I have the pleasure of assisting today?")
    global user_name
    user_name=input("Name: ")
    print()
    print(f'Well, hello there {user_name}, I am QuikEatz. I will be assisting you with your meal preperation for today.')
    print(f"QuikEatz is all inclusive meal planner. I will let you know when it's time to eat.")

def get_identity():
    identity_list=[]
    global user_species
    user_species=input("What do you identify as? Please reply with only the name of your identity. " )
    if len(user_species)>1:
        identity_list.append(user_species)

    while True:
        if len(user_species)>1:
            print(f'{user_name} the {user_species}, I will be planning a meal for you.')
            break
        else:
            print("QuikEatz does not currently support that life form. Please choose a species from the list")
            user_species=input("What do you identify as? Please reply with only the name of your identity." )
def convert():
    #optional 12-hour time support
    time=input("What time is it? ")
    if time.endswith('a.m.') is True:
        value, half=time.split(' ')
        hours, mins=value.split(":")
    elif time.endswith('p.m.') is True:
        value, half=time.split(' ')
        hours, mins=value.split(":")
        hours=int(hours)+12
    else:
        hours, mins=time.split(":")
    hours=int(hours)
    mins=int(mins)
    global time_value
    time_value=round(hours+mins/60,2)
    return time_value

if __name__=="__main__":
    main()
