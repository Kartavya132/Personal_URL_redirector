import func.function as fnf
from sys import exit
import os


def clear_screen():
    """Clear terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Print styled header"""
    print("\n" + "=" * 50)
    print("  🌐 PERSONAL URL REDIRECTOR 🌐".center(50))
    print("=" * 50 + "\n")


def print_menu():
    """Print main menu"""
    print("📋 MAIN MENU")
    print("-" * 50)
    print("  [1] 👤 Admin Panel (Manage URLs)")
    print("  [2] 🔗 View & Open URLs")
    print("  [3] ❌ Exit")
    print("-" * 50)


def main():
    fnf.load_data()

    while True:
        clear_screen()
        print_header()
        print_menu()

        choice = input("\n➤ Enter your choice (1-3): ").strip()

        if choice == "1":
            fnf.admin()
        elif choice == "2":
            fnf.view_and_open_urls()
        elif choice == "3":
            print("\n✓ Thank you for using URL Redirector. Goodbye! 👋\n")
            break
        else:
            print("\n❌ Invalid choice! Please enter 1, 2, or 3.")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
