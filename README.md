# git-swap

`git-swap` is a small CLI for switching between multiple Git identities on one device.

## Quick start

```sh
./git-swap add personal --name "Your Name" --email you@example.com
./git-swap add work --name "Your Work Name" --email you@company.com
./git-swap list
./git-swap use work
./git-swap current
```

Profiles are saved in `$XDG_CONFIG_HOME/git-swap/profiles.json` (or `~/.config/git-swap/profiles.json`) and switching updates Git's global `user.name` and `user.email`.

## Commands

```text
git-swap add <profile> --name <name> --email <email> [--force]
git-swap list
git-swap use <profile>
git-swap current
git-swap remove <profile>
```

To use it from anywhere, put this directory on your `PATH`, or install the `git-swap` launcher into a directory already on your `PATH`.
