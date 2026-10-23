"""Ask a vision-capable model about an image supplied on the command line."""

import sys
from pathlib import Path

from PIL import Image
from smolagents import CodeAgent

from common import make_model


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python 05_vision_agent.py path\\to\\image.png")

    image_path = Path(sys.argv[1])
    if not image_path.is_file():
        raise SystemExit(f"Image မတွေ့ပါ: {image_path}")

    agent = CodeAgent(tools=[], model=make_model(vision=True), max_steps=3)
    with Image.open(image_path) as source:
        image = source.convert("RGB")
        answer = agent.run("Describe what is in this image.", images=[image])
    print(f"\nFinal answer: {answer}")
