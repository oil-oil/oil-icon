#!/bin/bash
# One-time setup: create the Python venv used by slice_icons.py
# (Pillow + numpy + scipy for slicing; rembg for soft/3D/photo cutout).
set -e
SK="$(cd "$(dirname "$0")/.." && pwd)"
VENV="$SK/.venv"
python3 -m venv "$VENV"
source "$VENV/bin/activate"
pip install --quiet --upgrade pip
pip install --quiet Pillow numpy scipy "rembg[cpu]"
echo "oil-icon venv ready: $VENV"
echo "slice with: $VENV/bin/python3 $SK/scripts/slice_icons.py <sheet>.png <outdir> --mode floodfill|rembg"
