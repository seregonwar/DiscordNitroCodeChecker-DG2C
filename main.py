import tkinter as tk  # Importing the tkinter library for creating a GUI
from gui import DiscordCodeCheckerGUI  # Importing the DiscordCodeCheckerGUI class from the gui module
import string  # Importing the string library for string manipulation
import random  # Importing the random library for generating random values
import httpx  # Asynchronous HTTP client library
import asyncio  # Library for writing single-threaded concurrent code using coroutines, multiplexing I/O access over sockets and other resources, running network clients and servers, and other related primitives
import concurrent.futures  # Library for parallel execution of tasks
import multiprocessing  # Library for launching new processes
import requests  # Library for making HTTP requests

# Discord webhook URL
discord_webhook_url = "Enter here your web hook"  # Placeholder for the Discord webhook URL

def generate_random_string(length):
    """
    Generates a random alphanumeric string of given length using only lowercase characters.

    Args:
        length (int): The length of the random string to generate.

    Returns:
        str: A random alphanumeric string of the specified length.
    """
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

async def generate_and_check_codes():
    """
    Generates and checks gift codes asynchronously.

    This function generates 1000 random gift codes and checks their validity using an asynchronous HTTP client.
    It sends the generated codes and their validity status to a Discord webhook.
    """
    character_set = string.ascii_lowercase + string.digits

    while True:
        # Generate codes
        codes = [''.join(random.choices(character_set, k=18)) for _ in range(1000)]
        print("Generated 1000 codes")

        async with httpx.AsyncClient() as client:
            tasks = [check_gift_code(code, client) for code in codes]
            results = await asyncio.gather(*tasks)

        for code, is_valid in zip(codes, results):
            print(f"Code: {code}, Valid: {is_valid}")
            await send_to_discord_webhook(f"https://discord.gift/{code}")

async def check_gift_code(code, client):
    """
    Checks if a gift code is valid.

    Args:
        code (str): The gift code to check.
        client (httpx.AsyncClient): An asynchronous HTTP client instance.

    Returns:
        bool: True if the gift code is valid, False otherwise.
    """
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    print(f"Checking code: {code}")
    response = await client.get(url)
    print(f"Response for {code}: {response.status_code}")
    if response.status_code == 200:
        return True
    return False

async def send_to_discord_webhook(message):
    """
    Sends a message to a Discord webhook.

    Args:
        message (str): The message to send to the Discord webhook.
    """
    async with httpx.AsyncClient() as client:
        payload = {
            "content": message
        }
        await client.post(discord_webhook_url, json=payload)
        print(f"Message sent to Discord webhook: {message}")

def check_gift_code_concurrent(code):
    """
    Checks if a gift code is valid (concurrently).

    Args:
        code (str): The gift code to check.

    Returns:
        bool: True if the gift code is valid, False otherwise.
    """
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    print(f"Checking code: {code}")
    print(f"Response for {code}: {response.status_code}")
    if response.status_code == 200:
        return True
    return False

def process_codes(codes):
    """
    Processes a batch of codes.

    Args:
        codes (list): A list of gift codes to process.

    Returns:
        list: A list of tuples containing the gift code and its validity status.
    """
    results = []
    for code in codes:
        is_valid = check_gift_code_concurrent(code)
        print(f"Code: {code}, Valid: {is_valid}")
        send_to_discord_webhook(f"https://discord.gift/{code}")
        results.append((code, is_valid))
    return results

async def main():
    total_batches = 100

    # Concurrent processing with asyncio
    tasks = [generate_and_check_codes() for _ in range(total_batches)]
    await asyncio.gather(*tasks)

    # Concurrent processing with multiprocessing
    with multiprocessing.Pool(processes=total_batches) as pool:
        for _ in range(total_batches):
            codes = [generate_random_string(18) for _ in range(1000)]
            results = pool.map(process_codes, [codes])[0]

    # Start the GUI after the other operations have been completed
    root = tk.Tk()
    app = DiscordCodeCheckerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    asyncio.run(main())
