#!/usr/bin/env sh
set -eu

target_dir="${XDG_BIN_HOME:-$HOME/.local/bin}"
mkdir -p "$target_dir"
cp "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)/git-swap" "$target_dir/git-swap"
chmod 755 "$target_dir/git-swap"
printf 'Installed git-swap to %s/git-swap\n' "$target_dir"
case ":${PATH:-}:" in
  *:"$target_dir":*) ;;
  *) printf 'Add this directory to your PATH: export PATH="%s:$PATH"\n' "$target_dir" ;;
esac
