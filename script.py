'''
This script unfollows the last 200 (or a specified limit) users that you are following.
It uses the GitHub API to fetch the list of users and then unfollows each user.
The script includes error handling and rate limiting to avoid hitting GitHub's API limits.
You can run this script periodically to manage your following list on GitHub.
Note: Be careful when running this script, as it will unfollow users without confirmation.
Note: This script is for educational purposes and should be used responsibly.
'''



import requests
import time

# Replace with your GitHub credentials
TOKEN = "GITHUB ACCESS TOKEN"  # Your GitHub Personal Access Token
USERNAME = "GITHUB USERNAME"   # Your GitHub Username

# Headers for authentication (GitHub API uses OAuth tokens)
HEADERS = {
    "Authorization": f"token {TOKEN}",  # Authorization header with token
    "Accept": "application/vnd.github.v3+json"  # API version
}

# Function to fetch the list of people you're following
# This function fetches the last 'limit' number of users you are following
def get_following(limit=200):
    """
    Fetches a list of the users that the authenticated GitHub user is following.

    Args:
    limit (int): The number of followings to retrieve (default is 200).

    Returns:
    list: A list of usernames of the people you are following.
    """
    url = f"https://api.github.com/users/{USERNAME}/following?per_page={limit}"
    response = requests.get(url, headers=HEADERS)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Return a list of usernames
        return [user["login"] for user in response.json()]
    else:
        print(f"Error fetching following list: {response.status_code}")
        return []  # Return an empty list if there was an error

# Function to unfollow users
def unfollow_users():
    """
    Unfollows the last 200 users that the authenticated user is following.
    """
    following = get_following(200)  # Get the list of the last 200 people you're following

    if not following:
        print("You're not following anyone!")
        return

    print(f"Unfollowing {len(following)} users...")

    # Iterate through the list of users and unfollow each
    for user in following:
        url = f"https://api.github.com/user/following/{user}"
        response = requests.delete(url, headers=HEADERS)

        # Check if the unfollow request was successful (status code 204)
        if response.status_code == 204:
            print(f"Unfollowed {user} successfully")
        else:
            # Print an error if unfollowing failed
            print(f"Failed to unfollow {user}: {response.status_code}")

        # Delay to avoid hitting GitHub's rate limit (1 second)
        time.sleep(1)

    print(" Done! Last 200 followings unfollowed. Have a nice day!")

# Run the script when executed directly
if __name__ == "__main__":
    unfollow_users()
