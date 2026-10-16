---
name: chatgpt-chrome-extension-recovery
description: Diagnose and recover the official ChatGPT Chrome extension on macOS when the Chrome Web Store reports that it cannot be downloaded or installed. Use for the official ChatGPT browser-control extension and Google’s official update service; do not use to bypass enterprise policy, browser security warnings, or install arbitrary extensions.
---

# ChatGPT Chrome Extension Recovery

Recover the official extension without third-party CRX files, repackaging, or developer-mode loading.

## Safety boundaries

- Confirm the target is the official ChatGPT extension. The expected Chrome extension ID at publication is `hehggadaopoacecdllhhajmbjkdcmajg`; re-check it against current official OpenAI documentation before changing configuration.
- Try the supported flow first: update the ChatGPT desktop app, then use **Settings → Computer Use → Install** for Chrome.
- Treat installation and local browser-configuration changes as separate actions. Explain the exact file and value, then obtain user confirmation immediately before closing Chrome, writing or removing the configuration, or triggering installation.
- Stop if Chrome is organization-managed, an administrator policy blocks the extension, the extension ID differs, or the Google update URL redirects somewhere unexpected.
- Never download a CRX from GitHub, mirrors, file-sharing sites, or extension-download services. Never disable browser security, bypass a safety interstitial, edit Chrome account data, or read cookies, passwords, or tokens.

## Diagnose before changing anything

1. Record the OS, browser family/version, active Chrome profile, ChatGPT desktop version, and exact error.
2. Check whether the extension already exists in any Chrome profile and whether it is enabled.
3. Check **Settings → Computer Use**. `Manage` means the extension connection is recognized; `Install` means setup is incomplete.
4. Determine whether the failure is the store page, network access to Google’s update service, browser policy, or the ChatGPT native-host connection.
5. If the store page alone is unavailable on macOS and the user requests the recovery path, read [references/macos-external-update.md](references/macos-external-update.md).

## Recovery path

Use Chrome’s supported external-extension preference mechanism to point only at Google’s official update service. Prefer `scripts/manage_external_update.py` over recreating the JSON manually.

- Run `status` first; it is read-only.
- After explicit confirmation, run `install --apply`. The script only creates the expected JSON and refuses to overwrite conflicting content.
- Restart Chrome so it can request the signed extension from Google.
- If Google’s update service is unreachable, report the network failure and ask the user to switch to a network where it is reachable. Do not choose or configure a VPN for them.
- Let the user review and accept Chrome’s extension permission prompt when one appears.

## Verify the outcome

Verify independently rather than relying on the presence of the configuration file:

- Chrome contains the extension under the expected ID and shows it enabled.
- The installed manifest uses `https://clients2.google.com/service/update2/crx` as its update URL.
- Chrome records the package as originating from the Web Store / official update service, not as unpacked.
- The ChatGPT desktop app shows **Manage** for Chrome after restart.
- The native messaging host exists and points to an OpenAI-managed local executable. Treat native-host repair as a separate ChatGPT desktop/plugin problem; do not fabricate the manifest.

Report which layer succeeded: configuration created, Google download completed, Chrome extension enabled, and ChatGPT connection established.

## Rollback

After confirmation, `remove --apply` removes only the exact recovery configuration created by this skill. It does not uninstall an already-installed extension. Use Chrome’s own extensions UI for uninstalling the extension.
