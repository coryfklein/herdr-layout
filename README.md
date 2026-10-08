# herdr-layout

A [Herdr](https://herdr.dev) plugin that gives a live terminal pane a readable width measured in character columns. It adds real Herdr margin panes around the current pane, so mouse selection stays within the content pane.

The margins run the plugin spacer directly, without starting a shell or loading `.zshrc`. They ignore typed input. Layout shortcuts also work after a margin is clicked and return focus to the content pane.
Width and position changes resize existing margin panes. Entering or leaving exact edge alignment changes the number of margins.

The default width is **90 columns**. The plugin watches the layout and reapplies the chosen width after terminal or sidebar resizing. It does not start, resume, or reconnect Codex; use `codex resume` yourself when you want that.

Layouts are tracked per pane, so multiple Codex sessions in the same Herdr server can use independent widths and alignment.
In a tab with other panes, the configured layout applies within the original pane’s region.

## Install

Requires Herdr 0.9 or later, Python 3, macOS or Linux.

```sh
herdr plugin install coryfklein/herdr-layout
```

For local development, `herdr plugin link ~/code/herdr-layout` links the checkout directly. The plugin uses Python's standard library, so there is no build step.

Focus a pane and invoke **Toggle column layout** from Herdr's plugin actions. Toggle again to remove the margins. The plugin offers these actions:

| Action | Effect |
| --- | --- |
| `toggle` | Add or remove margins in the current tab |
| `wider` / `narrower` | Change the requested width by the configured step |
| `reset-width` | Restore the configured default width |
| `move-left` / `move-right` | Shift by the configured step where Herdr permits |
| `align-left` / `align-right` | Put the pane at the edge of its layout region |
| `center` | Center the pane |

For a shell wrapper that launches an interactive program, the executable also
accepts idempotent `enter` and `leave` commands. They use the current pane's
`HERDR_SOCKET_PATH` and `HERDR_PANE_ID` and run synchronously, so a wrapper
can enter the layout, run the program, then restore the pane when it exits.

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

Herdr supports direct `[[keys.command]]` bindings for plugin actions, with no leader key. If your terminal passes Command-arrow chords through to Herdr, add them to `~/.config/herdr/config.toml`:

```toml
[[keys.command]]
key = "cmd+shift+left"
type = "plugin_action"
command = "coryfklein.herdr-layout.move-left"
description = "move layout left by configured step"

[[keys.command]]
key = "cmd+shift+right"
type = "plugin_action"
command = "coryfklein.herdr-layout.move-right"
description = "move layout right by configured step"

[[keys.command]]
key = "cmd+shift+up"
type = "plugin_action"
command = "coryfklein.herdr-layout.wider"
description = "widen layout by configured step"

[[keys.command]]
key = "cmd+shift+down"
type = "plugin_action"
command = "coryfklein.herdr-layout.narrower"
description = "narrow layout by configured step"

[[keys.command]]
key = "ctrl+cmd+shift+left"
type = "plugin_action"
command = "coryfklein.herdr-layout.align-left"
description = "align layout left"

[[keys.command]]
key = "ctrl+cmd+shift+right"
type = "plugin_action"
command = "coryfklein.herdr-layout.align-right"
description = "align layout right"
```

The physical shortcuts depend on what your terminal sends to Herdr. Add bindings for `toggle`, `reset-width`, and `center` in the same way.

### Ghostty on macOS

Herdr requests the Kitty keyboard protocol, which lets Ghostty send Command-modified arrows directly to the `cmd` bindings above. Ghostty already leaves Cmd+Shift+Left/Right and Cmd+Ctrl+Shift+Left/Right free. Its default Cmd+Shift+Up/Down bindings jump between shell prompts, so free just those two chords in Ghostty's `config.ghostty`:

```ini
keybind = super+shift+arrow_up=unbind
keybind = super+shift+arrow_down=unbind
```

`super` is Ghostty's name for Command. Reload Ghostty's config, then run `herdr server reload-config` after changing Herdr's bindings. See [Ghostty's keybinding syntax](https://ghostty.org/docs/config/keybind) and [Herdr's keyboard guide](https://herdr.dev/docs/keyboard/) for other terminals or chords.

Herdr currently clamps each split to at least 10% of its parent. Edge alignment uses a single margin pane and reaches the layout region’s edge. Between an edge and the nearest position allowed by a three-pane layout, a small move cannot be represented; the first move inward jumps to the nearest allowed position.

## Development

```sh
python3 -m unittest discover -s tests
```

## Credits

The original layout approach was adapted from [herdr-zen](https://github.com/y4m3/herdr-zen), licensed under MIT. See [LICENSE](LICENSE).
