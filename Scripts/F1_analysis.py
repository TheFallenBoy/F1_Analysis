import os


def main():
    while True:
        os.system('clear')
        print("Please enter a number:")
        print("1.")
        print("2.")
        print("3.")
        print("4.")
        print("5.")
        print("6.")
        print("7.")
        print("8.")
        print("9.")
        print("0. Exit")
        choice = input()
        if not choice.isnumeric():
            print("Invalid Input")
            print("Press Enter to continue")
            input()
            continue
        choice = int(choice)
        if choice == 1:
            print("choice 1")
        elif choice == 2:
            print("choice 2")
        elif choice == 3:
            print("choice 3")
        elif choice == 4:
            print("choice 4")
        elif choice == 5:
            print("choice 5")
        elif choice == 6:
            print("choice 6")
        elif choice == 7:
            print("choice 7")
        elif choice == 8:
            print("choice 8")
        elif choice == 9:
            print("choice 9")
        elif choice == 0:
            print("Exiting program...")
            break
        else:
            print("invalid choice")
        

        print("Press Enter to continue")
        input()








if __name__ == '__main__':
    main()

