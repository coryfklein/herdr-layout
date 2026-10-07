# herdr-layout

A [Herdr](https://herdr.dev) plugin that gives a live terminal pane a readable width measured in character columns. It moves the pane into a dedicated tab with real Herdr margin panes, so mouse selection stays within the content pane. The process and scrollback remain attached to the original pane.

The default width is **90 columns**. The plugin watches the layout and reapplies the chosen width after terminal or sidebar resizing. It does not start, resume, or reconnect Codex; use `codex resume` yourself when you want that.

## Install

Requires Herdr 0.9 or later, Python 3, macOS or Linux.

```sh
herdr plugin install coryfklein/herdr-layout
```

For local development, `herdr plugin link ~/code/herdr-layout` links the checkout directly. The plugin uses Python's standard library, so there is no build step.

Focus a pane and invoke **Toggle column layout** from Herdr's plugin actions. Toggle again to put that same pane back in its original tab. The plugin offers these actions:

| Action | Effect |
| --- | --- |
| `toggle` | Enter or leave the dedicated layout tab |
| `wider` / `narrower` | Change the requested width by the configured step |
| `reset-width` | Restore the configured default width |
| `move-left` / `move-right` | Shift by one column where Herdr permits |
| `align-left` / `align-right` | Put the pane at the terminal edge |
| `center` | Center the pane |

## Width settings

Create `config.json` in the directory printed by `herdr plugin config-dir coryfklein.herdr-layout`:

```json
{
  "columns": 90,
  "resize_step": 10
}
```

`columns` must be at least 40; `resize_step` must be positive. Changes take effect on the next action. Use `reset-width` to apply a new default to an active layout.

When the available terminal area is too narrow, the plugin uses the widest pane Herdr can fit. It returns to the requested column width when the area grows.

## Keyboard shortcuts

Herdr supports direct `[[keys.command]]` bindings for plugin actions, so no leader key or plugin code change is required. Add whichever chords you prefer to `~/.config/herdr/config.toml`:

```toml
[[keys.command]]
key = "alt+shift+left"
type = "plugin_action"
command = "coryfklein.herdr-layout.move-left"
description = "move layout left one column"

[[keys.command]]
key = "alt+shift+right"
type = "plugin_action"
command = "coryfklein.herdr-layout.move-right"
description = "move layout right one column"

[[keys.command]]
key = "ctrl+alt+shift+left"
type = "plugin_action"
command = "coryfklein.herdr-layout.align-left"
description = "align layout left"

[[keys.command]]
key = "ctrl+alt+shift+right"
type = "plugin_action"
command = "coryfklein.herdr-layout.align-right"
description = "align layout right"
```

Add bindings for `toggle`, `wider`, `narrower`, `reset-width`, and `center` in the same way. Then run `herdr server reload-config`. Herdr's key strings can also use `cmd`, but the actual sequence depends on your terminal. Ghostty may need to translate Command chords before Herdr sees them.

Herdr currently clamps each split to at least 10% of its parent. Edge alignment uses a single margin pane and reaches the actual edge. Between an edge and the nearest position allowed by a three-pane layout, a one-column move cannot be represented; the first move inward jumps to the nearest allowed position.

## Development

```sh
python3 -m unittest discover -s tests
```

## Credits

The pane move and placeholder approach was adapted from [herdr-zen](https://github.com/y4m3/herdr-zen), licensed under MIT. See [LICENSE](LICENSE).
