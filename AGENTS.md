> For Mintlify product knowledge (components, configuration, writing standards),
> install the Mintlify skill: `npx skills add https://mintlify.com/docs`

# Documentation project instructions

## About this project

- This is the documentation site for [Otter Shell](https://git.pika-os.com/otter-shell) on [Mintlify](https://mintlify.com)
- Pages are MDX files with YAML frontmatter
- Configuration lives in `docs.json`
- Source reference code lives at `/home/ferreo/otter-shell` (each component is an independent git repo)
- Use the Mintlify MCP server, `https://mcp.mintlify.com`, to edit content and settings via MCP

## Terminology

- Use **Otter Shell** for the desktop environment (not "Otter" alone in headings)
- Use **pikman** for end-user installation (`pikman install otter-shell`), not `apt install`
- **`otter-shell`** is the base metapackage; **`otter-shell-extras`** adds `otter-transcribe` and `otter-vox` only
- Otter Shell does **not** ship a compositor. Do not document River or any compositor as the default.
- The greeter (`otter-greeter`) uses Hyprland for the login screen only. User sessions use their own compositor.

## Style preferences

- Use active voice and second person ("you")
- Keep sentences concise. One idea per sentence.
- Use sentence case for headings
- Bold for UI elements: Click **Settings**
- Code formatting for file names, commands, paths, and code references
- Base documentation on component READMEs in the otter-shell source. Do not invent features or package contents.

## Content boundaries

- Document packaged components only unless marked as workspace-only (`otter-dock`, `otter-hypr`, `otter-theme-gen`)
- Do not claim packages are in metapackages when debian/control says otherwise
- Developer docs belong in the Developer Guide tab
