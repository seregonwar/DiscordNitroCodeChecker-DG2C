# Discord Gift Code Checker - DG2C

This program is designed to automatically generate and verify Discord gift codes. It uses Discord's APIs to check the validity of the generated codes and sends the results to a Discord webhook.

## Features

### Gift Code Generation

The program generates a series of gift codes using a combination of lowercase characters and digits. Below is an example of a function that generates a gift code:

```python
def generate_random_string(length):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
```



The generated codes are verified through HTTP requests to Discord's APIs. Below is an example of a function that verifies a gift code using asyncio:

### Discord Gift Code Checker

```python
async def check_gift_code(code, client):
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = await client.get(url)
    if response.status_code == 200:
        return True
    return False
```

### Sending Results to Discord

If a code is valid, the program sends a message containing the code and a direct link to the gift code on Discord. Below is an example of a function that sends a message to a Discord webhook:

```python
async def send_to_discord_webhook(message):
    async with httpx.AsyncClient() as client:
        payload = {
            "content": message
        }
        await client.post(discord_webhook_url, json=payload)
```

## Code Generation Techniques

The program utilizes various techniques to generate a large number of gift codes efficiently.

### Random Generation

Gift codes are randomly generated by selecting characters from the allowed character set. Below is an example of random generation of a gift code:

```python
codes = [''.join(random.choices(character_set, k=18)) for _ in range(1000)]
```

### Concurrent Generation

To speed up the generation process, the program employs concurrency. Below is an example of concurrent generation of gift codes using asyncio:

```python
async with httpx.AsyncClient() as client:
    tasks = [check_gift_code(code, client) for code in codes]
    results = await asyncio.gather(*tasks)
```

### User Interface

After generating and verifying the gift codes, the program starts a user interface to display the results. Below is an example of starting the graphical user interface using Tkinter:

```python
root = tk.Tk()
app = DiscordCodeCheckerGUI(root)
root.mainloop()
```
[![Readme Card](https://github-readme-stats.vercel.app/api/pin/?username=seregonwar&repo=DiscordNitroCodeChecker-DG2C&theme=dark)](https://github.com/seregonwar/DiscordNitroCodeChecker-DG2C)



