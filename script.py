import requests
import time
import sys
from art import *
from termcolor import colored
import random
import datetime
import os

# Replace with your GitHub credentials
TOKEN = "YOUR_TOKEN"  # Your GitHub Personal Access Token
USERNAME = "YOUR_USERNAME"  # Your GitHub Username

# Headers for authentication (GitHub API uses OAuth tokens)
HEADERS = {
    "Authorization": f"token {TOKEN}",  # Authorization header with token
    "Accept": "application/vnd.github.v3+json"  # API version
}

AUTHOR_NAME = "Nibir Mahmud"
AUTHOR_GITHUB = "github.com/mahmudnibir"
AUTHOR_PROJECT = "CleanUpFollowing"

def print_AUTHOR_info():
    """Displays AUTHOR information in a cool way."""
    print(colored("\n📌 Author:", 'yellow'), colored(AUTHOR_NAME, 'cyan'))
    print(colored("🔗 GitHub:", 'yellow'), colored(AUTHOR_GITHUB, 'cyan'))
    print(colored("🛠️ Project:", 'yellow'), colored(AUTHOR_PROJECT, 'cyan'))
    print(colored("=" * 100, 'magenta'))

def animated_logo(text="Unfollow"):
    """Prints the logo with a typing animation effect."""
    logo = text2art(text)  # Generate ASCII text
    for char in logo:
        sys.stdout.write(colored(char, 'cyan'))  # Print each character with color
        sys.stdout.flush()  # Force output without waiting for a new line
        time.sleep(0.002)  # Adjust speed (lower = faster)


# Uncomment it if you want static logo

# def print_logo():
#     logo = text2art("Unfollow Following")
#     colored_logo = colored(logo, 'cyan')  # Change 'cyan' to your preferred color
#     print(colored_logo)


def progress_bar(iteration, total, prefix='', length=50, fill='█'):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    
    if iteration / total > 0.8:
        color = 'green'
    elif iteration / total > 0.5:
        color = 'yellow'
    else:
        color = 'red'
        
    sys.stdout.write(f'\r{prefix} |{colored(bar, color)}| {percent}% Complete')
    sys.stdout.flush()
    if iteration == total:
        print()  # Newline after progress bar

def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor

def show_spinner(spinner):
    sys.stdout.write("\rWorking... " + next(spinner))
    sys.stdout.flush()

def get_user_input():
    try:
        limit = int(input("How many users would you like to unfollow? (default 200): "))
    except ValueError:
        limit = 200  # Default to 200 if the user enters an invalid value
    return limit

def get_following(limit=300):
    url = f"https://api.github.com/users/{USERNAME}/following?per_page={limit}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        return [user["login"] for user in response.json()]
    else:
        print(colored(f"Error fetching following list: {response.status_code}", 'red'))
        return []

def log_unfollow(user, status):
    with open("unfollow_log.txt", "a") as file:
        file.write(f"Unfollowed {user}: {status}\n")

def retry_request(url, headers, retries=3):
    attempt = 0
    while attempt < retries:
        response = requests.delete(url, headers=headers)
        if response.status_code == 204:
            return True
        print(f"Retrying... Attempt {attempt + 1}")
        attempt += 1
        time.sleep(5)
    return False

def preview_unfollow(following):
    print("Here's a preview of the users to unfollow:")
    for user in following:
        print(f"- {user}")
    confirm = input("Do you want to continue? (y/n): ")
    return confirm.lower() == 'y'

def confirm_unfollow():
    confirm = input("Do you want to unfollow users? (y/n): ")
    if confirm.lower() != 'y':
        print("Operation canceled.")
        return False
    return True

def show_fun_message():
    messages = [
        "Good job, you're cleaning up!",
        "Haters gonna hate, but you're unfollowing them!",
        "You’ve got this! Keep going!",
        "Don't worry, you're not alone... everybody's unfollowing someone!"
    ]
    print(colored(random.choice(messages), 'yellow'))

def completion_message():
    print(colored("\nAll done! You’ve successfully unfollowed users. Stay tidy!", 'magenta'))

def unfollow_users():
    
    following = get_following(get_user_input())

    if not following:
        print("You're not following anyone!")
        return

    if not preview_unfollow(following):
        return

    if not confirm_unfollow():
        return

    print(f"Unfollowing {len(following)} users...")

    spinner = spinning_cursor()

    for i, user in enumerate(following, 1):
        show_spinner(spinner)
        time.sleep(0.1)

        url = f"https://api.github.com/user/following/{user}"
        response = requests.get(url, headers=HEADERS)
        if retry_request(url, HEADERS):
            log_unfollow(user, "Success")
            print(colored(f"\nUnfollowed {user} successfully", 'green'))
        else:
            log_unfollow(user, f"Failed: {response.status_code}")
            print(colored(f"\nFailed to unfollow {user}: {response.status_code}", 'red'))

        progress_bar(i, len(following), prefix='Progress')

        if i % 5 == 0:
            show_fun_message()

    completion_message()

# Run the script when executed directly
if __name__ == "__main__":
    animated_logo("Unfollow Following")
    print_AUTHOR_info()  # Display AUTHOR info
#     time.sleep(1)
#     print_logo()
    print("Welcome to the Unfollow Script!")
    print("This script unfollows users you are following on GitHub.")
    print("Note: Be careful, this will unfollow users without confirmation.")
#     time.sleep(1)
    unfollow_users()
