import func.function as fnf
from sys import exit


def main():
    print("|-------------------------------|")
    print("|---Welcome to our web helper---|")
    print("|-------------------------------|\n")

    ch = input("Press Enter to continue or 1 to admin : ")
    if ch == "1":
        fnf.admin()
    fnf.choice()


if __name__ == "__main__":
    main()
