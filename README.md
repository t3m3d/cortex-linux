# cortex

A GUI file manager for Linux, written in **pure [Krypton](https://krypton-lang.org)**
talking the **X11 wire protocol directly** — no libX11, no xcb, no toolkit.
Linux-locked on purpose; built for and used on Hyprland (Xwayland).

The X11 client layer lives in the Krypton stdlib (`stdlib/x11.k`): connect over
the `/tmp/.X11-unix` socket, CreateWindow/MapWindow, GCs, FillRect, ImageText8,
PutImage, FillArc, properties (WM_CLASS / WM_NAME / WM_PROTOCOLS / _NET_WM_ICON),
and the event loop. The whole UI — icons, theming, compositing — is drawn by
cortex itself.

## Build & run

```sh
./build.ks                  # builds ./cortex (KryptScript build script)
CORTEX_RUN=1 ./build.ks     # builds ./cortex and launches it
CORTEX_OUT=/tmp/cortex ./build.ks   # custom output path
# or, manually:
KRYPTON_ROOT=~/path/to/krypton \
  ~/path/to/krypton/bootstrap/kcc_driver_linux_x86_64 cortex.k -o /tmp/cortex
/tmp/cortex
```

`build.ks` defaults `KRYPTON_ROOT` to `../krypton`; override it if your
checkout is elsewhere. It runs via `kcc -r` (`#!/usr/bin/env -S kcc -r`, on
PATH from the Homebrew krypton install); the output path and run-after-build
are set with the `CORTEX_OUT` / `CORTEX_RUN` env vars (the `-r` runner doesn't
forward CLI args).

Requires (runtime, optional but recommended): `ImageMagick` (`magick`/`convert`)
+ `xxd` for crisp raster icons, `gio`/`udisksctl` for trash & drive mounting,
`xdg-open` to open files, `git` for repo status/actions, `inotifywait` for
auto-refresh, `wofi`/`fzf` for Open With, and a terminal for "open terminal here".

## Features

- **Icon grid & list views** (Tab, or Ctrl+1 / Ctrl+2; choice persists)
- **Quick-access sidebar** — Home/Desktop/Documents/… plus your bookmarks; the
  current location is highlighted
- **GTK bookmarks + XDG user dirs** — reads `~/.config/gtk-3.0/bookmarks` and
  `xdg-user-dir` locations
- **External drives** — removable partitions via `lsblk` (mounted or not);
  right-click to mount/unmount, Ctrl+M mounts all
- **File-type icons** — distinct glyphs for folders, images, archives, audio/
  video, and generic files (dirs listed first)
- **Toolbar** — back / forward / reload + a typeable address bar
- **Git integration** — branch + ahead/behind in status bar, per-file status
  badges in list view, context-menu Git Status/Pull/Push
- **Sort** — name / size / date / kind, ascending/descending (Ctrl+S cycle,
  Ctrl+Shift+S toggle direction; persisted)
- **Multi-select** — Space marks, Ctrl+A all; bulk copy / cut / trash
- **Fuzzy filter & search** — type to filter with fuzzy matching, Enter to
  search subfolders
- **Command palette** — Ctrl+K for quick actions/commands
- **Preview pane** — Ctrl+P toggles bottom text/file preview
- **File actions** — copy/cut/paste (no-clobber), rename, bulk rename (editor),
  trash, new file/folder, duplicate, compress to zip, extract archive, open
  terminal here, Open With
- **Checksums & info** — Copy MD5/SHA-256, folder size, properties from context menu
- **Inspect/compare** — hex view, text/markdown/json/yaml preview, duplicate finder,
  folder compare, chmod/attributes, color labels, saved searches
- **Auto-refresh** — inotify-based directory watch when `inotifywait` is available
- **Thumbnails groundwork** — freedesktop thumbnail cache helpers for images/PDFs
- **D-Bus helper** — `cortex-filemanager1.py` for org.freedesktop.FileManager1
- **Light / dark theming** — from `~/.config/cortex/config` (`theme=dark|light|
  auto`) then system settings
- **Session persistence** — last directory, view, sort, sort direction, hidden files

## Hyprland

- **Dropdown/scratchpad mode**: set `dropdown=1` in config or run with
  `CORTEX_DROPDOWN=1`. Cortex sets title `cortex-dropdown` and applies Hyprland
  window rules (float, special workspace, slide animation, centered 80%x60%).
- **Suggested bind**:
  ```ini
  bind = SUPER, E, exec, CORTEX_DROPDOWN=1 cortex
  # or toggle special workspace if you keep it running:
  bind = SUPER, E, togglespecialworkspace, cortex
  ```
- **Window rules**: class is `cortex`; title is `cortex` (normal) or
  `cortex-dropdown` (dropdown mode).

## Keyboard shortcuts

| Key | Action |
|-----|--------|
| Enter / double-click | open file or folder |
| Backspace | go up |
| Alt+Left / Alt+Right | back / forward |
| Alt+Home | home folder |
| type a name | jump to it |
| arrows / PageUp/Down / Home / End | move selection |
| Tab, Ctrl+1 / Ctrl+2 | toggle / set icon & list view |
| Space | mark / unmark item |
| Ctrl+A / Ctrl+Shift+A | select all / clear selection |
| Delete / F8 | move selection (or item) to trash |
| Ctrl+C / Ctrl+X / Ctrl+V | copy / cut / paste (no-clobber) |
| Ctrl+N / Ctrl+Shift+N / F7 | new file / new folder (then type the name) |
| Ctrl+Shift+R | duplicate |
| Ctrl+E / Ctrl+Shift+Z | extract archive / compress to zip |
| F2 | rename |
| Ctrl+I | properties |
| Ctrl+Shift+C | copy path |
| Ctrl+H | toggle hidden files |
| Ctrl+S / Ctrl+Shift+S | cycle sort / toggle sort direction |
| Ctrl+F | search (Enter = include subfolders) |
| F5 | refresh |
| Ctrl+D / Ctrl+Shift+D | bookmark / unbookmark current dir |
| Ctrl+Shift+T | trash view |
| Ctrl+M | mount all removable drives |
| Ctrl+L | edit address bar |
| F4 | open terminal here |
| F1 | this help overlay |
| Ctrl+W / Ctrl+Q / Esc | clear selection, then close |

## Context menu

Right-click a file/folder for: Open, Open With, Cut, Copy, Paste, Rename,
Bulk Rename, Move to Trash, New Folder, Open Terminal, Duplicate, Compress,
Properties, Copy MD5, Copy SHA-256, Folder Size, Git Status, Git Pull, Git Push.

## Config

`~/.config/cortex/config` (key=value):

```ini
theme=dark|light|auto
accent=#1FA463
terminal=foot
opener=xdg-open
dropdown=0
```

`~/.config/cortex/` also stores:
- `bookmarks` — one path per line (managed via Ctrl+D / Ctrl+Shift+D)
- `lastdir` — restored on launch
- `view` — `grid` or `list`
- `sort` — `name`, `size`, `date`, or `kind`
- `sortasc` — `1` or `0`
- `hidden` — `1` or `0`

## Desktop integration

Install `cortex.desktop` to `~/.local/share/applications/` for launcher/menu
integration and `inode/directory` handling. `cortex-filemanager1.py` provides a
minimal org.freedesktop.FileManager1 session service.

## Not yet ported

- Dual pane / tabs
- Xdnd drag-and-drop
- Embedded PTY terminal / SFTP browser
- Marquee select
- Full Git panel GUI (stage/unstage/discard/commit UI)
- Native PDF/Quick Look preview
- Smart collections UI / advanced saved search UI
- Full thumbnail rendering in grid/list

Excluded: Cortex Vaults.
