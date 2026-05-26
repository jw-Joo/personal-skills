# kc-manual Map

Use this reference when the repository has the standard kc-manual structure.

## Repository Shape

- `source/index.rst`: top-level Sphinx index.
- `source/applet/*.rst`: Applet Console and IoT SAFE manuals.
- `source/applet/images/...`: screenshots used by Applet manuals.
- `_build/`: generated output. Do not edit by hand.

## Common Release Terms To Search

- Login/logout: `ログアウト`, `ログイン`, `自動ログアウト`, `セッション`.
- eSIM/eIM: `eSIM`, `eIM`, `プロファイル`, `有効化`, `無効化`, `eIM Action`, `最終アクション`, `Withdrawn`.
- SIM/Poller/OTA: `SIM`, `Poller`, `Poller名`, `OTA`, `Displayed after OTA`, `CSVエクスポート`.
- IoT SAFE Client: `iotsafe-client`, `system diagnose`, `vpn`, `get-iccid`, `download-config`, `CA証明書`, `OpenVPN`.
- Settings/API: `設定`, `API`, `通知`, `アクセス`, `証明書`.

## Likely Target Files

| Release area | Likely file |
| --- | --- |
| Logout/session behavior | `source/applet/console_logout.rst` |
| eSIM list/detail, eIM, profile actions | `source/applet/console_esim.rst` |
| SIM list/detail/search/export, Poller display, OTA execution | `source/applet/console_sim.rst` |
| OTA applet registration/versioning | `source/applet/console_ota.rst` |
| IoT SAFE Client CLI commands | `source/applet/iot_safe_client.rst` |
| IoT SAFE console menu | `source/applet/console_iot_safe*.rst` |
| Console settings | `source/applet/console_setting.rst` |

## RST Style Notes

- Preserve existing heading adornment style in the file.
- Keep list-table indentation exactly aligned.
- Existing files often use `|` lines for spacing; follow local style instead of normalizing.
- Avoid broad copyediting in unrelated sections.
- Use existing Japanese UI labels exactly as they appear in the manual or screenshots.

## Screenshot Handling

- Prefer descriptive filenames under the existing feature folder.
- Update image paths relative to the `.rst` file, usually `images/...`.
- Preserve or add `:scale:` only when needed to match nearby screenshots.
- Do not copy release-note screenshots that only duplicate existing images without visible behavior changes.
