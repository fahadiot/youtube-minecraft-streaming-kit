# Contributing

Contributions are welcome! This is a small, single-file project, so the
process is simple:

1. Fork the repo and create a new branch for your change.
2. Make your change. If you're adding a new reaction/feature, follow the
   existing pattern in `minecraft_youtube_bot.py`:
   - Add a new `ENABLE_...` toggle read from an environment variable.
   - Document it in `.env.example` and in the README's feature table.
3. Test it against your own YouTube channel and Minecraft server before
   opening a PR.
4. Open a pull request describing what changed and why.

## Ideas for contributions

- Support for other server hosts besides Exaroton (e.g. via RCON for
  self-hosted servers).
- Additional reactions (super chats, membership events, comments, etc).
- A Discord webhook notification alongside the in-game reaction.

## Reporting issues

Open a GitHub issue with:
- What you expected to happen
- What actually happened (include console output, with your API keys
  redacted)
- Your Python version and OS
