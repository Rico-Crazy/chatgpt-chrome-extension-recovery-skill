# ChatGPT Chrome Extension Recovery Skill

A Codex skill for diagnosing and recovering the official ChatGPT Chrome extension on macOS when the Chrome Web Store reports that the item cannot be downloaded or installed.

The recovery method uses Chrome’s external-extension preference mechanism and points only to Google’s official update service. It does not bundle a CRX, download from mirrors, use developer mode, or bypass enterprise policy.

## Install the skill

```bash
git clone https://github.com/Rico-Crazy/chatgpt-chrome-extension-recovery-skill.git
cp -R chatgpt-chrome-extension-recovery-skill ~/.codex/skills/chatgpt-chrome-extension-recovery
```

Restart Codex, then invoke:

```text
$chatgpt-chrome-extension-recovery diagnose why the official ChatGPT Chrome extension will not install.
```

## Safety model

- Read-only diagnosis comes first.
- The normal OpenAI installation flow is preferred.
- Configuration changes require explicit user confirmation.
- The helper script is dry-run by default and refuses to overwrite or remove unexpected content.
- Chrome permission prompts remain user-reviewed.
- No personal paths, browser history, credentials, or machine logs are included in this repository.

## Helper script

Check current state:

```bash
python3 scripts/manage_external_update.py status
```

Preview configuration creation:

```bash
python3 scripts/manage_external_update.py install
```

After reviewing the exact target and granting approval:

```bash
python3 scripts/manage_external_update.py install --apply
```

The skill contains the full diagnosis, verification, and rollback workflow.

## Scope

This repository is for the official ChatGPT Chrome extension on macOS. It is not a general-purpose browser-extension installer and should not be used to bypass organizational or browser security controls.

## License

MIT

