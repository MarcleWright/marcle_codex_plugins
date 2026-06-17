# WSY Codex Plugins

This directory is a local Codex plugin marketplace.

## Install on a device

1. Add this marketplace root in Codex:

```powershell
codex plugin marketplace add D:\00_Projects_WSY\AI\Codex_Projects\marcle_codex_plugins
```

2. Install the plugin from this marketplace:

```powershell
codex plugin add image-gen-openai-hk@marcle-codex-plugins
```

3. Configure the API key on that device using one of these options:

```powershell
$env:OPENAI_HK_IMAGE_KEY="your_key_here"
```

or create one of these files:

```text
D:\00_Projects_WSY\AI\Codex_Projects\marcle_codex_plugins\plugins\image-gen-openai-hk\.env
<home>\.image-gen-openai-hk.env
```

with:

```text
openai-hk_image_key=your_key_here
```

Do not commit or share the real `.env` file.
