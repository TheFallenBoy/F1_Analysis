import os


def main():
    choices = {
                "1" : fastest_average_pit_stop,
                "2" : won_most_races,
                "3" : most_wins_driver,
                "4" : avg_pit_stop_time,
                "5" : add_pit_stop_time,
                "6" : total_championship_points,
            }


    while True:
        os.system('clear')
        print("""Please enter a number:\n1.\n2.\n3.\n4.\n5.\n6.\n0.\n""")
        choice = input()
        if choice.isnumeric() and int(choice) == 0:
            break
        if choice in choices:
            choices[choice]()
        else:
            print("Invalid input")
        print("Press Enter to continue")
        input()



def fastest_average_pit_stop():
    print("fastest average pit stop")

def won_most_races():
    print("most_races")

def most_wins_driver():
    print("most_wins")

def avg_pit_stop_time():
    print("avg pit stop")

def add_pit_stop_time():
    print("pit stop time")

def total_championship_points():
    print("constructor")




if __name__ == '__main__':
    main()

