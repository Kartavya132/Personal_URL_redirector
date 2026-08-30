import pandas as pd

URL_DATA = "data/url.csv"


def load_data():
    global url_dataset
    try:
        url_dataset = pd.read_csv(URL_DATA)
        if url_dataset.empty:
            print("Warning: CSV file is empty")
    except FileNotFoundError:
        print("There is no such file go and create it")
        url_dataset = None


def admin():
    global url_dataset

    print("---------------------")
    print("Welcome to Admin page\n")

    choice = input("Enter what is your wants : ")

    if "add" in choice or "new" in choice:
        print("\nAdding a new data of url.\n")
    elif "delete" in choice or "remove" in choice:
        print("\nDeleting a data of url.\n")
    elif "view" in choice or "see" in choice:
        print("\nThese is the data::-\n")
    else:
        print("Enter Valid choice.")


def choice():
    pass


if __name__ == "__main__":
    print("You came in wrong file go to the main.py")
