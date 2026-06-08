# Source: https://git.pika-os.com/otter-shell/otter-zenith/src/branch/main/main.sh

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-zenith](https://git.pika-os.com/otter-shell/otter-zenith)

Watch [1](https://git.pika-os.com/otter-shell/otter-zenith/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-zenith/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-zenith/forks)

You've already forked otter-zenith

generated from [wm-packages/river](https://git.pika-os.com/wm-packages/river)

**Files**

**main**

![](https://git.pika-os.com/avatars/27248cd7565f39f4ba9b1a494e1fec8522d00a274df18a3c3221d181631669ad?size=48) [**ferreo**](https://git.pika-os.com/ferreo 'ferreo') [ea6924b385](https://git.pika-os.com/otter-shell/otter-zenith/commit/ea6924b3852b22f7b8b1049dcfcc005f10146e61) [Update main.sh](https://git.pika-os.com/otter-shell/otter-zenith/commit/ea6924b3852b22f7b8b1049dcfcc005f10146e61)

2026-06-08 21:31:05 +02:00

#### 

59 lines

3.9 KiB

Bash

Executable File

[Raw](https://git.pika-os.com/otter-shell/otter-zenith/raw/branch/main/main.sh) [Permalink](https://git.pika-os.com/otter-shell/otter-zenith/src/commit/6ac96c31eddd04a52dc3e796c452b658121a0f60/main.sh) [Blame](https://git.pika-os.com/otter-shell/otter-zenith/blame/branch/main/main.sh) [History](https://git.pika-os.com/otter-shell/otter-zenith/commits/branch/main/main.sh)

| | `#! /bin/bash` |
| --- | --- |
| | |
| | `set -e` |
| | |
| | `. ./pika-build-config.sh` |
| | |
| | `echo "$PIKA_BUILD_ARCH" > pika-build-arch` |
| | |
| | `VERSION="0.11.14"` |
| | `# Create workspace` |
| | `mkdir -p otter-shell-"$VERSION"` |
| | |
| | `# Clone each application at tagged release` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-bar.git otter-shell-"$VERSION"/otter-bar` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-launcher.git otter-shell-"$VERSION"/otter-launcher` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-notifications.git otter-shell-"$VERSION"/otter-notifications` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-wallpaper.git otter-shell-"$VERSION"/otter-wallpaper` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-osd.git otter-shell-"$VERSION"/otter-osd` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-logout.git otter-shell-"$VERSION"/otter-logout` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-settings.git otter-shell-"$VERSION"/otter-settings` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-polkit.git otter-shell-"$VERSION"/otter-polkit` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-lock.git otter-shell-"$VERSION"/otter-lock` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-idle.git otter-shell-"$VERSION"/otter-idle` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-term.git otter-shell-"$VERSION"/otter-term` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-jade.git otter-shell-"$VERSION"/otter-jade` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-screenshot.git otter-shell-"$VERSION"/otter-screenshot` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-shot.git otter-shell-"$VERSION"/otter-shot` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-cal.git otter-shell-"$VERSION"/otter-cal` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-calc.git otter-shell-"$VERSION"/otter-calc` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-clip.git otter-shell-"$VERSION"/otter-clip` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-emoji.git otter-shell-"$VERSION"/otter-emoji` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-note.git otter-shell-"$VERSION"/otter-note` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-pick.git otter-shell-"$VERSION"/otter-pick` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-rec.git otter-shell-"$VERSION"/otter-rec` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-timer.git otter-shell-"$VERSION"/otter-timer` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-weather.git otter-shell-"$VERSION"/otter-weather` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-transcribe.git otter-shell-"$VERSION"/otter-transcribe` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-vox.git otter-shell-"$VERSION"/otter-vox` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-desktop.git otter-shell-"$VERSION"/otter-desktop` |
| | `git clone --depth 1 -b v"$VERSION" https://git.pika-os.com/otter-shell/otter-greeter.git otter-shell-"$VERSION"/otter-greeter` |
| | |
| | `cp -rvf ./debian ./otter-shell-"$VERSION"/` |
| | `cp -rvf ./fonts ./otter-shell-"$VERSION"/` |
| | `cp -rvf ./vendor ./otter-shell-"$VERSION"/` |
| | `cd ./otter-shell-"$VERSION"` |
| | |
| | `apt-get install nvidia-cuda-dev -y` |
| | `# Get build deps` |
| | `LOGNAME=root dh_make --createorig -y -l -p otter-shell_"$VERSION" || echo "dh-make: Ignoring Last Error"` |
| | `apt-get build-dep ./ -y` |
| | |
| | `# Build package` |
| | `dpkg-buildpackage --no-sign` |
| | |
| | `# Move the debs to output` |
| | `cd ../` |
| | `mkdir -p ./output` |
| | `mv ./*.deb ./output/` |

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-zenith/blame/commit/6ac96c31eddd04a52dc3e796c452b658121a0f60/main.sh) [Copy Permalink]()