import pandas as pd
from urllib.parse import urlparse
import requests
import webbrowser
import os

URL_DATA = "data/url.csv"
url_dataset = None


def clear_screen():
    """Clear terminal screen"""
    os.system("cls" if os.name == "nt" else "clear")


def load_data():
    global url_dataset
    try:
        url_dataset = pd.read_csv(URL_DATA)
        if url_dataset.empty:
            url_dataset = pd.DataFrame(columns=["name", "url"])
    except FileNotFoundError:
        print("📁 CSV file not found. Creating new database...")
        url_dataset = pd.DataFrame(columns=["name", "url"])
        url_dataset.to_csv(URL_DATA, index=False)


def check_url(url):
    """Validate and check if URL is reachable"""
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        return False, "Invalid URL format"
    try:
        r = requests.head(url, timeout=5, allow_redirects=True)
        if r.status_code >= 400:
            return False, f"Unreachable (Status {r.status_code})"
    except requests.RequestException as e:
        return False, f"Connection error: {str(e)[:40]}"
    return True, "✓ Valid"


def display_urls_table():
    """Display all URLs in a formatted table"""
    global url_dataset

    if url_dataset is None or url_dataset.empty:
        print("📭 No URLs saved yet.\n")
        return False

    print("\n" + "=" * 70)
    print(f"{'#':<4} {'Name':<20} {'URL':<44}")
    print("=" * 70)

    for idx, row in url_dataset.iterrows():
        url_preview = row["url"][:41] + "..." if len(row["url"]) > 41 else row["url"]
        print(f"{idx:<4} {row['name']:<20} {url_preview:<44}")

    print("=" * 70 + "\n")
    return True


def add_url():
    """Add a new URL"""
    global url_dataset

    print("\n📝 ADD NEW URL")
    print("-" * 50)

    name = input("➤ Enter URL name: ").strip()
    while not name:
        print("❌ Name cannot be empty!")
        name = input("➤ Enter URL name: ").strip()

    # Check if name already exists
    if name.lower() in url_dataset["name"].str.lower().values:
        print(f"❌ URL name '{name}' already exists!")
        return

    while True:
        url = input("➤ Enter the URL: ").strip()
        if not url:
            print("❌ URL cannot be empty!")
            continue

        valid, reason = check_url(url)
        if valid:
            print(f"✓ URL is valid!")
            break
        print(f"❌ Invalid URL ({reason}). Try again.")

    url_dataset.loc[len(url_dataset)] = [name, url]
    url_dataset.to_csv(URL_DATA, index=False)
    print(f"\n✓ Successfully added: {name} → {url}\n")


def delete_url():
    """Delete a URL entry"""
    global url_dataset

    if not display_urls_table():
        return

    print("🗑️  DELETE URL")
    print("-" * 50)

    try:
        delete_index = int(input("➤ Enter the # of URL to delete: "))

        if delete_index < 0 or delete_index >= len(url_dataset):
            print("❌ Invalid index. Please try again.\n")
            return

        deleted_name = url_dataset.loc[delete_index, "name"]
        url_dataset = url_dataset.drop(delete_index).reset_index(drop=True)
        url_dataset.to_csv(URL_DATA, index=False)
        print(f"✓ Successfully deleted: {deleted_name}\n")

    except ValueError:
        print("❌ Invalid input. Please enter a valid number.\n")


def view_url_details():
    """View detailed information about a URL"""
    global url_dataset

    if not display_urls_table():
        return

    print("📊 VIEW DETAILS")
    print("-" * 50)

    try:
        idx = int(input("➤ Enter the # of URL to view: "))

        if idx < 0 or idx >= len(url_dataset):
            print("❌ Invalid index.\n")
            return

        row = url_dataset.loc[idx]
        print(f"\nName: {row['name']}")
        print(f"URL:  {row['url']}")

        valid, reason = check_url(row["url"])
        status = f"✓ {reason}" if valid else f"❌ {reason}"
        print(f"Status: {status}\n")

    except ValueError:
        print("❌ Invalid input.\n")


def view_and_open_urls():
    """View and open URLs"""
    global url_dataset

    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("  🔗 VIEW & OPEN URLs".center(50))
        print("=" * 50)

        if not display_urls_table():
            input("Press Enter to return to main menu...")
            return

        print("📋 OPTIONS")
        print("-" * 50)
        print("  [1] 🌐 Open URL in browser")
        print("  [2] 📊 View URL details")
        print("  [3] ← Back to Main Menu")
        print("-" * 50)

        choice = input("➤ Enter your choice: ").strip()

        if choice == "1":
            try:
                idx = int(input("➤ Enter the # of URL to open: "))
                if 0 <= idx < len(url_dataset):
                    url = url_dataset.loc[idx, "url"]
                    print(f"\n🌐 Opening {url} in browser...")
                    webbrowser.open(url)
                    print("✓ URL opened!\n")
                    input("Press Enter to continue...")
                else:
                    print("❌ Invalid index.\n")
            except ValueError:
                print("❌ Invalid input.\n")
        elif choice == "2":
            view_url_details()
        elif choice == "3":
            return
        else:
            print("❌ Invalid choice.\n")


def admin():
    """Admin panel for managing URLs"""
    global url_dataset

    while True:
        clear_screen()
        print("\n" + "=" * 50)
        print("  👤 ADMIN PANEL".center(50))
        print("=" * 50)

        display_urls_table()

        print("📋 ADMIN MENU")
        print("-" * 50)
        print("  [1] ➕ Add new URL")
        print("  [2] 🗑️  Delete URL")
        print("  [3] 📊 View URL details")
        print("  [4] ← Back to Main Menu")
        print("-" * 50)

        choice = input("➤ Enter your choice (1-4): ").strip()

        if choice == "1":
            add_url()
            input("Press Enter to continue...")
        elif choice == "2":
            delete_url()
            input("Press Enter to continue...")
        elif choice == "3":
            view_url_details()
            input("Press Enter to continue...")
        elif choice == "4":
            break
        else:
            print("❌ Invalid choice! Please enter 1-4.\n")
            input("Press Enter to continue...")
