"""
YouTube Minecraft Streaming Kit
--------------------------------
Watches a YouTube channel/video for new subscribers and likes while you're
live, and reacts on your Minecraft server (hosted via Exaroton) in real time.

All secrets are read from environment variables (see .env.example) -
nothing sensitive is hardcoded in this file.

FEATURES (turn any of these on/off in your .env file, no code editing needed):
  ENABLE_KILL_ON_SUB     -> new subscriber kills all players
  ENABLE_CREEPER_ON_LIKE -> new like summons a creeper
  ENABLE_SPAWN_RESET     -> keeps everyone's spawn point up to date each cycle

Want to add your OWN reaction to a sub or a like? Jump to the
"ADD YOUR OWN ACTIONS HERE" section near the bottom of this file.
"""

import os
import time

import requests
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

# ---------------------------------------------------------------------------
# REQUIRED CONFIG (must be set in your .env file)
# ---------------------------------------------------------------------------
GOOGLE_API_KEY = os.environ["GOOGLE_API_KEY"]
CHANNEL_ID = os.environ["CHANNEL_ID"]
VIDEO_ID = os.environ["VIDEO_ID"]
EXAROTON_API_TOKEN = os.environ["EXAROTON_API_TOKEN"]
EXAROTON_SERVER_ID = os.environ["EXAROTON_SERVER_ID"]

# ---------------------------------------------------------------------------
# FEATURE TOGGLES - set to "true" or "false" in your .env file
# ---------------------------------------------------------------------------
ENABLE_KILL_ON_SUB = os.environ.get("ENABLE_KILL_ON_SUB", "true").lower() == "true"
ENABLE_CREEPER_ON_LIKE = os.environ.get("ENABLE_CREEPER_ON_LIKE", "true").lower() == "true"
ENABLE_SPAWN_RESET = os.environ.get("ENABLE_SPAWN_RESET", "true").lower() == "true"

# ---------------------------------------------------------------------------
# OPTIONAL CONFIG - safe to leave as default
# ---------------------------------------------------------------------------
# In-game username the creeper should spawn near. Defaults to all players.
TARGET_PLAYER = os.environ.get("TARGET_PLAYER", "@a")

# How often to poll YouTube's API, in seconds. Keep this reasonably high -
# the YouTube Data API has a limited daily free quota.
POLL_INTERVAL_SECONDS = int(os.environ.get("POLL_INTERVAL_SECONDS", "30"))

youtube = build("youtube", "v3", developerKey=GOOGLE_API_KEY)


def send_command_to_server(command: str) -> None:
    """Send a console command to the Exaroton-hosted Minecraft server."""
    url = f"https://api.exaroton.com/v1/servers/{EXAROTON_SERVER_ID}/command"
    headers = {
        "Authorization": f"Bearer {EXAROTON_API_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json={"command": command}, timeout=10)
    if response.status_code == 200:
        print(f"[server] sent: {command}")
    else:
        print(f"[server] failed to send '{command}': {response.status_code} {response.text}")


def get_subscriber_count() -> int:
    request = youtube.channels().list(part="statistics", id=CHANNEL_ID)
    response = request.execute()
    return int(response["items"][0]["statistics"]["subscriberCount"])


def get_like_count() -> int:
    request = youtube.videos().list(part="statistics", id=VIDEO_ID)
    response = request.execute()
    return int(response["items"][0]["statistics"]["likeCount"])


# ---------------------------------------------------------------------------
# REACTIONS - what happens on each event
# ---------------------------------------------------------------------------
def on_new_subscriber() -> None:
    print("New subscriber detected!")
    send_command_to_server("/say A new subscriber has entered the arena!")
    if ENABLE_KILL_ON_SUB:
        send_command_to_server("/kill @e[type=minecraft:player]")

    # --- ADD YOUR OWN ACTIONS HERE (subscriber events) ---
    # Example: send_command_to_server("/summon lightning_bolt ~ ~ ~")


def on_new_like() -> None:
    print("New like detected!")
    if ENABLE_CREEPER_ON_LIKE:
        send_command_to_server(f"/execute at {TARGET_PLAYER} run summon creeper ~ ~2 ~")

    # --- ADD YOUR OWN ACTIONS HERE (like events) ---
    # Example: send_command_to_server(f"/effect give {TARGET_PLAYER} minecraft:speed 10")


def reset_spawn_for_all() -> None:
    if ENABLE_SPAWN_RESET:
        send_command_to_server("/execute at @a run spawnpoint @s ~ ~ ~")


# ---------------------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------------------
def main() -> None:
    print("Starting YouTube -> Minecraft bridge...")
    print(f"  Kill all players on new sub : {ENABLE_KILL_ON_SUB}")
    print(f"  Summon creeper on new like  : {ENABLE_CREEPER_ON_LIKE}")
    print(f"  Auto spawn reset each cycle : {ENABLE_SPAWN_RESET}")

    last_subs = get_subscriber_count()
    last_likes = get_like_count()
    print(f"Initial subscriber count: {last_subs}")
    print(f"Initial like count: {last_likes}")

    while True:
        try:
            current_subs = get_subscriber_count()
            print(f"Subscribers: {current_subs}")
            if current_subs > last_subs:
                on_new_subscriber()
            last_subs = current_subs

            current_likes = get_like_count()
            print(f"Likes: {current_likes}")
            if current_likes > last_likes:
                on_new_like()
            last_likes = current_likes

            reset_spawn_for_all()
        except Exception as exc:
            print(f"Error during poll cycle: {exc}")

        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
