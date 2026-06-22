---
name: image-generation-openai
description: "Use the local OpenAI-HK curl-compatible script for gpt-image-2 by default, with Gemini/nano-banana when requested."
license: MIT
metadata:
  tags: [image-generation, openai-hk, gpt-image-2, nano-banana, gemini, curl, creative]
---

# Image Gen OpenAI-HK

Use this skill by default when the user asks Codex to generate, draw, create, or edit raster images with GPT Image 2, OpenAI-HK, Gemini/nano-banana, or a curl-style image API workflow.

Important default rule for this user:

- If the user says "生图", "画图", "生成图片", "改图", "图生图", "做海报", "做视觉图", "生成概念图", or similar image generation/editing language, use this skill and the local script by default.
- Default to `gpt-image-2`.
- Use Gemini/nano-banana only when the user mentions "nano-banana", "nanobanana", "nano banana", or "gemini", or explicitly asks for a nano-banana model.
- Do not use Codex's built-in/default image generation when the user asks for this OpenAI-HK / gpt-image-2 path.
- Exception: if the user explicitly asks Codex to create SVG/vector/code-native art, follow that request instead.

## What this skill does

Calls the local plugin wrapper script from this installed plugin. Resolve the plugin root from this `SKILL.md` path:

```text
<plugin-root>/skills/image-generation-openai/SKILL.md
<plugin-root>/scripts/gpt_image_2_curl.py
```

When working from the shared source checkout on this machine, the script is:

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "PROMPT"
```

The script targets:

```text
https://api.openai-hk.com/v1/images/generations
https://api.openai-hk.com/v1/images/edits
```

Defaults:

```text
model = gpt-image-2
quality = medium
size = 1024x1024
response_format = url
output = <home>/Pictures/codex-generated/image-gen-openai-hk/<session-project-folder>
```

Gemini/nano-banana defaults when requested:

```text
provider = nano-banana
model = nano-banana-2
quality = low
size = 16x9
```

## Requirements

The API key may be supplied through any of these options:

```text
OPENAI_HK_IMAGE_KEY environment variable
openai-hk_image_key environment variable
openai-hk_image_key in the plugin root .env file
openai-hk_image_key in <home>/.image-gen-openai-hk.env
```

Never print the API key back to the user. If showing curl examples, use the script's `--show-curl` option or redact the key.

## Text-to-image

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "a futuristic electric sedan concept, silver body, studio lighting"
```

Useful parameters:

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "PROMPT" --model gpt-image-2 --size 1024x1024 --quality medium
```

## Gemini / nano-banana

Only use nano-banana when the user mentions "nano-banana", "nanobanana", "nano banana", or "gemini".

The script can infer nano-banana from the prompt text, but passing `--provider nano-banana` or `--nano-banana` is clearer when Codex has already decided the request is for Gemini/nano-banana:

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "a white siamese cat" --provider nano-banana --size 9x16
```

Model selection:

```text
default -> nano-banana-2
mentions 2k or --k 2K -> nano-banana-2-2k
mentions 4k or --k 4K -> nano-banana-2-4k
```

Supported nano-banana sizes:

```text
4x3
3x4
16x9
9x16
2x3
3x2
```

For ratio wording, pass `--ratio`; the script converts `9:16` to the nano-banana API's `9x16` format:

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "gemini nano-banana product poster, 2k" --ratio 9:16 --k 2K
```

Direct curl shape for nano-banana text-to-image:

```powershell
curl.exe -X POST "https://api.openai-hk.com/v1/images/generations" `
  -H "Authorization: Bearer ${env:OPENAI_HK_IMAGE_KEY}" `
  -H "Content-Type: application/json" `
  -d '{"model":"nano-banana-2","prompt":"a white siamese cat","n":1,"size":"9x16","quality":"low"}'
```

## Show curl example

To show a redacted curl command without making the API request:

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "a white siamese cat" --show-curl
```

Direct curl shape for text-to-image:

```powershell
curl.exe -X POST "https://api.openai-hk.com/v1/images/generations" `
  -H "Authorization: Bearer ${env:OPENAI_HK_IMAGE_KEY}" `
  -H "Content-Type: application/json" `
  -d '{"model":"gpt-image-2","prompt":"a white siamese cat","n":1,"size":"1024x1024","quality":"medium","response_format":"url"}'
```

For nano-banana, `--show-curl` emits the nano-banana JSON payload and omits `response_format`.

## Ratio plus K auto sizing

If the user specifies a ratio and K level, pass both with `--ratio` and `--k`.

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "汽车概念图" --ratio 16:9 --k 2K
```

This maps to:

```text
2048x1152
```

Supported mappings:

```text
1:1 1K -> 1024x1024
1:1 2K -> 2048x2048
1:1 4K -> 2880x2880
16:9 1K -> 1280x720
16:9 2K -> 2048x1152
16:9 4K -> 3840x2160
9:16 1K -> 720x1280
9:16 2K -> 1152x2048
9:16 4K -> 2160x3840
5:4 1K -> 1040x832
5:4 2K -> 2080x1664
5:4 4K -> 3200x2560
4:5 1K -> 832x1040
4:5 2K -> 1664x2080
4:5 4K -> 2560x3200
4:3 1K -> 1024x768
4:3 2K -> 2048x1536
4:3 4K -> 3264x2448
3:4 1K -> 768x1024
3:4 2K -> 1536x2048
3:4 4K -> 2448x3264
3:2 1K -> 1008x672
3:2 2K -> 2064x1376
3:2 4K -> 3504x2336
2:3 1K -> 672x1008
2:3 2K -> 1376x2064
2:3 4K -> 2336x3504
21:9 1K -> 1344x576
21:9 2K -> 2016x864
21:9 4K -> 3808x1632
```

## Image edit / image-to-image

For one or more reference images, repeat `--image`:

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "Generate a photorealistic product poster using the reference images" --image C:/path/ref1.png --image C:/path/ref2.png
```

This calls `/v1/images/edits` and sends files as `image[]` form fields.

For nano-banana image editing, pass `--provider nano-banana` and repeat `--image` for each reference:

```powershell
python D:/00_Projects_WSY/AI/Codex_Projects/marcle_codex_plugins/plugins/image-gen-openai-hk/scripts/gpt_image_2_curl.py "Generate a photorealistic image of a gift basket on a white background labeled Relax & Unwind" --provider nano-banana --image C:/path/body-lotion.png --image C:/path/bath-bomb.png --image C:/path/incense-kit.png --image C:/path/soap.png
```

Direct curl shape for image editing:

```powershell
curl.exe -X POST "https://api.openai-hk.com/v1/images/edits" `
  -H "Authorization: Bearer ${env:OPENAI_HK_IMAGE_KEY}" `
  -F "model=gpt-image-2" `
  -F "image[]=@C:/path/ref1.png" `
  -F "prompt=Generate a photorealistic product poster"
```

Direct curl shape for nano-banana image editing:

```powershell
curl.exe -X POST "https://api.openai-hk.com/v1/images/edits" `
  -H "Authorization: Bearer ${env:OPENAI_HK_IMAGE_KEY}" `
  -F "model=nano-banana-2" `
  -F "prompt=Generate a photorealistic product poster" `
  -F "image[]=@C:/path/ref1.png" `
  -F "image[]=@C:/path/ref2.png"
```

## Response handling

The script prints JSON like:

```json
{
  "success": true,
  "mode": "generation",
  "provider": "gpt-image",
  "model": "gpt-image-2",
  "size": "2048x1152",
  "quality": "medium",
  "paths": ["<home>/Pictures/codex-generated/image-gen-openai-hk/<session-project-folder>/openai-hk_gpt-image-2_YYYYMMDD_HHMMSS_1.png"],
  "urls": ["https://...png"],
  "usage": {}
}
```

After a successful generation, tell the user the saved image path and render it in the Codex app with Markdown image syntax when useful:

```markdown
![generated image](C:/absolute/path/to/image.png)
```

## Failure handling

If the script reports that no API key is set, ask the user to add `openai-hk_image_key=your_key` to:

```text
the installed plugin root .env file, or <home>/.image-gen-openai-hk.env
```

If the API returns an HTTP error, report the error directly and do not invent an image result.
