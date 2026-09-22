# YouTube Minecraft Streaming Kit

> Guys, I made this script a few years ago for my own YouTube channel and it
> worked perfectly fine! I was hosting my Minecraft server on the free tier of
> Exaroton (originally I looked at Aternos too), and ran this script behind
> the scenes while it stayed connected to my YouTube live stream. Every time
> someone subscribed or liked the video, something would happen in-game in
> real time - it made streams way more chaotic and fun. Cleaned it up and
> open-sourced it so anyone can plug in their own channel and server and use
> it too.

Connect a live YouTube stream to a Minecraft server. Every time you get a new
**subscriber**, all players get killed. Every time you get a new **like**, a
creeper gets summoned. Great for chaotic subathon-style streams.

> **Note on server hosts:** this kit talks to [Exaroton](https://exaroton.com/)'s
> console API to run commands on your server. It will **not** work with Aternos,
> since Aternos doesn't provide a public API for sending server commands.
> Exaroton has a small free tier, so it's an easy drop-in replacement if you're
> currently on Aternos.

## Demo

[Watch it in action here](https://youtu.be/7HNHVjpOMKs?t=1397)

## What you need

- Python 3.9+
- A Minecraft server hosted on [Exaroton](https://exaroton.com/)
- A YouTube channel and (optionally) a specific live video to watch

## Setup

1. **Clone this repo**
   ```
   git clone https://github.com/your-username/youtube-minecraft-streaming-kit.git
   cd youtube-minecraft-streaming-kit
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Create your `.env` file**
   ```
   cp .env.example .env
   ```
   Then open `.env` and fill in the values below.

4. **Run it**
   ```
   python minecraft_youtube_bot.py
   ```

## Where to get each value

| Variable | Where to get it |
|---|---|
| `GOOGLE_API_KEY` | Go to [Google Cloud Console](https://console.cloud.google.com/) → create a project → enable **YouTube Data API v3** → go to *Credentials* → *Create Credentials* → *API key*. |
| `CHANNEL_ID` | Open your YouTube channel page → *Settings* → *Advanced settings*, or use a tool like [commentpicker.com/youtube-channel-id](https://commentpicker.com/youtube-channel-id.php) with your channel URL. |
| `VIDEO_ID` | The part of your video URL after `watch?v=`. Example: `youtube.com/watch?v=abc123` → `VIDEO_ID=abc123`. |
| `EXAROTON_API_TOKEN` | Log in to [Exaroton](https://exaroton.com/) → *Account* → *API* → generate a new token. |
| `EXAROTON_SERVER_ID` | In the Exaroton dashboard, click your server → the server ID is shown in the URL and on the server's *Overview* page. |
| `TARGET_PLAYER` *(optional)* | Your in-game Minecraft username, if you only want the creeper to spawn near you. Leave as `@a` to target everyone. |
| `POLL_INTERVAL_SECONDS` *(optional)* | How often (in seconds) the bot checks YouTube for changes. Default is `30`. |

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

## License

MIT - do whatever you want with it, just don't blame us if a creeper ruins your build.
