#!/usr/bin/env python3
"""Switch between named global Git identities."""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

CONFIG_PATH = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "git-swap" / "profiles.json"


def load_profiles():
    if not CONFIG_PATH.exists():
        return {"profiles": {}, "active": None}
    try:
        data = json.loads(CONFIG_PATH.read_text())
        return {"profiles": data.get("profiles", {}), "active": data.get("active")}
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Could not read {CONFIG_PATH}: {exc}") from exc


def save_profiles(data):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2) + "\n")
    os.chmod(CONFIG_PATH, 0o600)


def git_config(key, value=None):
    command = ["git", "config", "--global", key]
    if value is not None:
        command.append(value)
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "git config failed")
    return result.stdout.strip()


def add(args):
    data = load_profiles()
    if args.profile in data["profiles"] and not args.force:
        raise RuntimeError(f"Profile '{args.profile}' already exists; use --force to replace it")
    data["profiles"][args.profile] = {"name": args.git_name, "email": args.email}
    save_profiles(data)
    print(f"Saved profile '{args.profile}'.")


def list_profiles(_args):
    data = load_profiles()
    if not data["profiles"]:
        print("No profiles yet. Add one with: git-swap add <profile> --name <name> --email <email>")
        return
    for profile, values in sorted(data["profiles"].items()):
        marker = " *" if profile == data.get("active") else ""
        print(f"{profile}{marker}\t{values['name']} <{values['email']}>")


def use(args):
    data = load_profiles()
    profile = data["profiles"].get(args.profile)
    if profile is None:
        raise RuntimeError(f"Profile '{args.profile}' does not exist")
    git_config("user.name", profile["name"])
    git_config("user.email", profile["email"])
    data["active"] = args.profile
    save_profiles(data)
    print(f"Switched to '{args.profile}' ({profile['name']} <{profile['email']}>).")


def remove(args):
    data = load_profiles()
    if args.profile not in data["profiles"]:
        raise RuntimeError(f"Profile '{args.profile}' does not exist")
    del data["profiles"][args.profile]
    if data.get("active") == args.profile:
        data["active"] = None
    save_profiles(data)
    print(f"Removed profile '{args.profile}'.")


def current(_args):
    data = load_profiles()
    if data.get("active"):
        print(data["active"])
    else:
        print("No active git-swap profile.")


def build_parser():
    parser = argparse.ArgumentParser(prog="git-swap", description="Switch between Git user profiles.")
    commands = parser.add_subparsers(dest="command", required=True)
    add_parser = commands.add_parser("add", help="save a profile")
    add_parser.add_argument("profile")
    add_parser.add_argument("--name", dest="git_name", required=True, help="Git user.name")
    add_parser.add_argument("--email", required=True, help="Git user.email")
    add_parser.add_argument("--force", action="store_true", help="replace an existing profile")
    add_parser.set_defaults(func=add)
    commands.add_parser("list", aliases=["ls"], help="list profiles").set_defaults(func=list_profiles)
    use_parser = commands.add_parser("use", help="activate a profile")
    use_parser.add_argument("profile")
    use_parser.set_defaults(func=use)
    current_parser = commands.add_parser("current", help="show the active profile")
    current_parser.set_defaults(func=current)
    remove_parser = commands.add_parser("remove", aliases=["rm"], help="delete a saved profile")
    remove_parser.add_argument("profile")
    remove_parser.set_defaults(func=remove)
    return parser


def main(argv=None):
    try:
        args = build_parser().parse_args(argv)
        args.func(args)
        return 0
    except RuntimeError as exc:
        print(f"git-swap: error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
