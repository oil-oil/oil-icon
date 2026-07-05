#!/usr/bin/env python3
"""External-API fallback provider: OpenAI Images (gpt-image).

Used only when the calling agent has no native image tool and Codex is not
available. For any other API (Replicate, Fal, Stability, …), call that API
directly instead — this script is just the ready-made OpenAI path.

  gen_image.py --prompt "<full sheet prompt>" --out raw/<style>.png

Reads OPENAI_API_KEY from the environment. No third-party deps (stdlib only).
"""
import argparse, base64, json, os, sys, urllib.request


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--model", default="gpt-image-1")
    ap.add_argument("--size", default="1024x1024")
    a = ap.parse_args()

    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        sys.exit("OPENAI_API_KEY is not set")

    body = json.dumps({"model": a.model, "prompt": a.prompt, "size": a.size, "n": 1}).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/images/generations",
        data=body,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        data = json.load(r)
    with open(a.out, "wb") as f:
        f.write(base64.b64decode(data["data"][0]["b64_json"]))
    print(a.out)


if __name__ == "__main__":
    main()
