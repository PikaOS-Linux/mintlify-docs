# otter-greeter

`otter-greeter` is Otter Shell's Wayland-only display manager. It installs:

- `otter-greeterd`: root daemon for PAM, logind seats, AccountsService, IPC, and session launch.
- `otter-greeter-ui`: unprivileged Wayland client hosted by configured greeter compositor.

## Install

Create dedicated system user `otter-greeter`, install binaries, then install:

- `/etc/otter-shell/otter-greeter.conf`
- `/etc/otter-shell/otter-greeter-hyprland.conf`
- `/etc/pam.d/otter-greeter`
- `/etc/pam.d/otter-greeter-autologin`
- `/usr/lib/systemd/system/otter-greeter.service`

Enable with `systemctl enable otter-greeter.service`.

## Configuration

Main config path: `/etc/otter-shell/otter-greeter.conf`.

Default greeter compositor: `/usr/bin/start-hyprland -- --config /etc/otter-shell/otter-greeter-hyprland.conf`.

Default display VT: `7`.

State path: `/var/lib/otter-greeter/state.conf`.

Runtime sockets: `/run/otter-greeter/<seat>.sock`.

Wayland sessions are discovered from configured `.desktop` directories. X11 sessions are ignored.

Autologin is attempted once per daemon process per seat. Failure falls back to normal interactive login.

AccountsService is preferred for user listing. If unavailable, passwd fallback includes normal login users and excludes non-login shells.

Fingerprint auth is PAM-controlled. Direct fprintd status must not grant login.

Expired-password flows are PAM conversation prompts rendered by same auth surface.

## License

MIT License — see [LICENSE](LICENSE).
