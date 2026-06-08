# Source: https://git.pika-os.com/otter-shell/otter-zenith/src/branch/main/release.sh

[otter-shell](https://git.pika-os.com/otter-shell)/[otter-zenith](https://git.pika-os.com/otter-shell/otter-zenith)

Watch [1](https://git.pika-os.com/otter-shell/otter-zenith/watchers)

Star [0](https://git.pika-os.com/otter-shell/otter-zenith/stars)

[Fork]() [0](https://git.pika-os.com/otter-shell/otter-zenith/forks)

You've already forked otter-zenith

generated from [wm-packages/river](https://git.pika-os.com/wm-packages/river)

**Files**

**main**

![](https://git.pika-os.com/assets/img/avatar_default.png) **Otter Shell** [6c7ce89c5e](https://git.pika-os.com/otter-shell/otter-zenith/commit/6c7ce89c5edb878e681bfcdc53e9355e7a0fc5ac) [Initial commit](https://git.pika-os.com/otter-shell/otter-zenith/commit/6c7ce89c5edb878e681bfcdc53e9355e7a0fc5ac)

2026-02-14 23:46:38 +01:00

#### 

4 lines

146 B

Bash

Executable File

[Raw](https://git.pika-os.com/otter-shell/otter-zenith/raw/branch/main/release.sh) [Permalink](https://git.pika-os.com/otter-shell/otter-zenith/src/commit/6ac96c31eddd04a52dc3e796c452b658121a0f60/release.sh) [Blame](https://git.pika-os.com/otter-shell/otter-zenith/blame/branch/main/release.sh) [History](https://git.pika-os.com/otter-shell/otter-zenith/commits/branch/main/release.sh)

| | `# send debs to server` |
| --- | --- |
| | `rsync -azP --include './' --include '*.deb' --exclude '*' ./output/ ferreo@direct.pika-os.com:/srv/www/cockatiel-incoming/` |
| | |

[Reference in New Issue]() [View Git Blame](https://git.pika-os.com/otter-shell/otter-zenith/blame/commit/6ac96c31eddd04a52dc3e796c452b658121a0f60/release.sh) [Copy Permalink]()