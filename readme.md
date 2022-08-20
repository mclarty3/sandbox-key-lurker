## Overview
---
Someone at Facepunch, popular game developers known for Garry's Mod and its upcoming successor, [S&Box](https://sbox.facepunch.com/news), has decided to change how the distribution of developer access tokens is handled. Keys are now released at seemingly random times, and are given to a random selection of how many people are present on the site when they are handed out.

Often, many people are eagerly waiting on the website for comparatively few keys to be given out, to be inevitably disappointed when they don't receive one. On top of this, many members of the S&Box Discord claim to be using bots to increase their chances of getting a key, flaunting how many keys they've gotten to the unfortunate many still waiting.

All of this being said, I made a bot to increase my chances of getting a key. But I promise if I get more than one I'll give out the extras without charging money and without bragging about it. I'll stoop, but not that low.

## What It Does
---
Given a list of steam credentials, this script will spawn multiple threads, each running a separate ChromeDriver instance. Each of these instances will log into Steam using the given credentials (no 2FA allowed, sorry!), and wait to join the S&Box Developer Preview queue. For the time being, each bot will just watch the queue forever, waiting until the "Enter" button is enabled, clicking it, then waiting unil the button is enabled again. They're very intelligent bots. I don't actually know what happens when you're granted a key, so I haven't implemented any behaviour for beyond that.

## Using It
---
Clone the repository.
```bash
git clone https://github.com/mclarty3/sandbox-key-lurker.git
```

Add a steam_creds.txt file to the root of the repository.
```bash
touch steam_creds.txt
```

The format should be as follows:
```bash
username1 password1
username2 password2
...
```

From there, you can simply run the script from the root directory.
```bash
/.../sandbox-key-lurker> python3 main.py
```

Good luck from there! As I mentioned above, I'm not sure what happens if you get given a key, but in theory once you receive one you can just quit the script and you'll have your key.

The following arguments can also be passed when running the script:
```
-h, --help          Display this help message
-H, --headless      Run the script in headless mode (browser GUIs will not open)
-s, --silent        Only output to console when bot is initialized and when queue is restarted or bot is killed
-S, --super-silent  The console won't output anything at all. Not sure why you'd want this, but just in case.
-r, --run-once      When the queue is restarted, kill the bot rather than waiting to join the next queue
```

When you want to exit the script, just mash Ctrl+C a bunch until the script quits. It takes a little while, sorry I'm not the best at Python threading.
