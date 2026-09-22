# YouTube Minecraft Streaming Kit

> Guys, I made this script a few years ago for my own YouTube channel and it
> worked perfectly fine! I was hosting my Minecraft server on the free tier of
> Exaroton (originally I looked at Aternos too), and ran this script behind
> the scenes while it stayed connected to my YouTube live stream. Every time
> someone subscribed or liked the video, something would happen in-game in
> real time - it made streams way more chaotic and fun. Cleaned it up and
> open-sourced it so anyone can plug in their own channel and server and use
> it too.

**What does this actually do?** It watches your YouTube channel in the
background. The moment someone new subscribes, everyone on your Minecraft
server dies. The moment someone likes your live video, a creeper appears
right next to you. That's it - no gaming experience or coding knowledge
needed to use it, just some patient copy-pasting of a few settings.

You do **not** need to know how to code to follow this guide. Every step is
spelled out in full, in the order you should do them. Just go top to bottom
and don't skip ahead.

**Stuck on anything, at any step?** Don't struggle alone - open an issue
here and describe exactly where you got stuck:
[Report a problem / ask for help](https://github.com/fahadiot/youtube-minecraft-streaming-kit/issues/new)

## Step 1: Star this repo

Before anything else, click the **☆ Star** button at the very top-right of
this page (it turns into a filled ★ once clicked). This costs nothing, takes
two seconds, and helps other people find this project too. Thank you!

## Demo

[Watch it in action here](https://youtu.be/7HNHVjpOMKs?t=1397) - watching
this first will help everything below make a lot more sense, since you'll
see exactly what the finished result looks and feels like.

> **Note on server hosts:** this kit talks to [Exaroton](https://exaroton.com/)'s
> console API to run commands on your server. It will **not** work with Aternos,
> since Aternos doesn't provide a public API for sending server commands.
> Exaroton has a small free tier, so it's an easy drop-in replacement if you're
> currently on Aternos.

## What you'll need before you start

Think of these as the four ingredients. You don't need to fully understand
what each one is yet - just know you'll be collecting all four as you follow
the steps:

1. A computer with internet access (Windows, Mac, or Linux all work)
2. A Minecraft server hosted on [Exaroton](https://exaroton.com/) (free tier is fine)
3. A YouTube channel that you own or manage
4. About 20-30 minutes of uninterrupted time, since some steps involve
   waiting for websites to load or approve things

## Step 2: Install Python

This script is written in a language called Python, so your computer needs
it installed to run the script at all.

1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click the big yellow "Download Python" button
3. Open the file you just downloaded and run it
4. **Important (Windows only):** on the very first install screen, tick the
   checkbox at the bottom that says **"Add Python to PATH"** before clicking
   Install. If you miss this, later steps will fail with a
   "python is not recognized" error - if that happens, just uninstall and
   reinstall Python, remembering to tick that box this time.
5. Click through the rest with the default options

To check it worked: open a terminal (Windows: search for "Command Prompt" in
your Start menu; Mac: search for "Terminal") and type:

```
python --version
```

then press Enter. If you see something like `Python 3.12.3`, it worked. If
you see an error instead, redo step 4 above.

## Step 3: Download this project onto your computer

You don't need to know git for this - just download it like a regular file:

1. Near the top of this page, click the green **"Code"** button
2. Click **"Download ZIP"**
3. Find the downloaded ZIP file (usually in your Downloads folder) and
   extract/unzip it (right-click it → "Extract All" on Windows, or just
   double-click it on Mac)
4. You should now have a folder called `youtube-minecraft-streaming-kit`
   somewhere on your computer. Remember where you put it - you'll need to
   open a terminal inside this exact folder in the next step.

## Step 4: Open a terminal inside the project folder

- **Windows:** open the `youtube-minecraft-streaming-kit` folder in File
  Explorer, click once in the empty address bar at the top (where the folder
  path is shown), type `cmd`, and press Enter. A black terminal window opens
  already pointed at the right folder.
- **Mac:** open the `youtube-minecraft-streaming-kit` folder in Finder,
  right-click inside it while holding the Option key, and choose
  "Open Terminal at Folder" (or open Terminal normally and type `cd ` then
  drag the folder into the window and press Enter).

## Step 5: Install the project's dependencies

Dependencies are just extra bits of code this project needs to run - Python
can install them all with one command. In the terminal you just opened,
type:

```
pip install -r requirements.txt
```

then press Enter and wait for it to finish (you'll see a lot of text scroll
by - that's normal).

## Step 6: Create your settings file

This project reads all its secret keys and settings from one file. To create
it, in the same terminal type:

```
cp .env.example .env
```

*(Windows users: if that command gives an error, use `copy .env.example .env`
instead - Windows uses a different command for copying files.)*

Now open the new `.env` file with a plain text editor (Notepad on Windows,
TextEdit on Mac both work fine - just don't use Microsoft Word). You'll fill
in the blanks in this file using the table in the next step.

## Step 7: Fill in your `.env` file

Go through this table one row at a time. For each one, find the matching
line in your `.env` file and paste the value after the `=` sign, with no
spaces and no quote marks around it.

| Setting | Where to get it |
|---|---|
| `GOOGLE_API_KEY` | Go to [Google Cloud Console](https://console.cloud.google.com/). If it's your first time, click through any "Welcome"/"Get Started" screens. Click **"Select a project"** at the top → **"New Project"** → give it any name (e.g. "minecraft-stream") → **Create**. Once created, make sure that project is selected at the top. Then use the search bar at the top and search for **"YouTube Data API v3"**, click it, then click **Enable**. Once enabled, in the left sidebar go to **Credentials** → **+ Create Credentials** → **API key**. A popup shows your new key - copy it. |
| `CHANNEL_ID` | Go to your own YouTube channel page while logged in → click **your profile picture** → **Settings** → **Advanced settings**. Your Channel ID is shown there. If you can't find it that way, paste your channel's URL into [commentpicker.com/youtube-channel-id](https://commentpicker.com/youtube-channel-id.php) and it will show you the ID. |
| `VIDEO_ID` | Open the specific YouTube video/livestream you want to track. Look at its URL - it looks like `youtube.com/watch?v=abc123XYZ`. Everything after `v=` is your Video ID (in that example, `abc123XYZ`). |
| `EXAROTON_API_TOKEN` | Log in at [exaroton.com](https://exaroton.com/) → click your account name (top right) → **Account** → **API** → **Create Token** → give it any name → copy the token shown (you'll only see it once, so copy it immediately). |
| `EXAROTON_SERVER_ID` | Still logged into Exaroton, click on your Minecraft server from your server list. Look at the web address in your browser - the server ID is the long code in the URL. It's also shown on the server's "Overview" page. |
| `TARGET_PLAYER` *(optional)* | Your in-game Minecraft username, if you only want the creeper to spawn near you specifically. If you leave this as `@a`, it affects everyone on the server instead. |
| `POLL_INTERVAL_SECONDS` *(optional)* | How often (in seconds) the script checks YouTube for new subs/likes. Leave this alone unless you know what you're doing - default is `30`. |

Save the `.env` file once every line is filled in.

## Step 8: Run it!

Back in your terminal (the one still open in the project folder), type:

```
python minecraft_youtube_bot.py
```

and press Enter. If everything above was done correctly, you'll see the
script start up and begin checking your channel. Leave this terminal window
open and running in the background while you're live - closing it stops the
script.

**Something not working?** Read the exact error message shown in the
terminal, then [open an issue here](https://github.com/fahadiot/youtube-minecraft-streaming-kit/issues/new)
and paste that error message in - that's the fastest way to get help.

## Turn features on/off - no coding required

Everything is controlled from your `.env` file. Just set any of these to
`true` or `false` and restart the script:

| Setting | What it does | Default |
|---|---|---|
| `ENABLE_KILL_ON_SUB` | Kills every player on the server when someone new subscribes | `true` |
| `ENABLE_CREEPER_ON_LIKE` | Summons a creeper near `TARGET_PLAYER` when the video gets a new like | `true` |
| `ENABLE_SPAWN_RESET` | Continuously resets everyone's spawn point to where they currently are, so deaths don't send them back to world spawn | `true` |

Want everyone to keep their normal spawn point? Set `ENABLE_SPAWN_RESET=false`.
Only want the creeper effect and not the sub-kill chaos? Set
`ENABLE_KILL_ON_SUB=false` and leave the rest on. Mix and match however you like.

## Want a custom reaction instead?

Open `minecraft_youtube_bot.py` and look for the two functions
`on_new_subscriber()` and `on_new_like()` - each has a clearly marked
`ADD YOUR OWN ACTIONS HERE` section where you can drop in any extra
`send_command_to_server("...")` call with any Minecraft command you want
(spawn fireworks, give items, teleport players, change the time of day, etc).
No other part of the file needs to change.

## How it works

- The bot polls the YouTube Data API on a timer (`POLL_INTERVAL_SECONDS`).
- If the subscriber count goes up, `on_new_subscriber()` runs (kill-all, if enabled).
- If the like count goes up, `on_new_like()` runs (creeper summon, if enabled).
- Every cycle, if enabled, it also resets each player's spawn point to their current location, so deaths don't send people back to the world spawn.

## A few notes

- The **free YouTube Data API quota** is limited (10,000 units/day). Checking every 30 seconds uses a small amount per call, but don't set `POLL_INTERVAL_SECONDS` too low or you may hit the daily limit.
- This is meant to run against **your own server** with **your own API keys** - never share your `.env` file or commit it to git.
- Commands are sent via Exaroton's console API, so your server must be online and the bot must have network access to `api.exaroton.com`.

## Still stuck?

Open an issue and describe what step you're on and what you're seeing:
[github.com/fahadiot/youtube-minecraft-streaming-kit/issues/new](https://github.com/fahadiot/youtube-minecraft-streaming-kit/issues/new)

## License

MIT - do whatever you want with it, just don't blame us if a creeper ruins your build.
