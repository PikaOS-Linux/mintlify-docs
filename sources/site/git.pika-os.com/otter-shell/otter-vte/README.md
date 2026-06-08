# otter-vte

Shared terminal rendering primitives for Otter Shell.

`otter-vte` owns terminal command buffering, custom terminal glyph drawing,
powerline/block cell primitives, and the generic terminal cell renderer used by
`otter-term`. PTY/session ownership and Ghostty integration stay in app code;
rendering paths live here so terminal views can be embedded by other apps
without copying Otter Term internals.

Text commands use `otter-render`'s shaped text path when callers attach a
`TextSystem` and `ShapeScratch` to `DynamicCommandList`, preserving fallback
fonts, CJK, RTL, and complex-script rendering through the shared renderer.

## License

MIT License — see [LICENSE](LICENSE).
