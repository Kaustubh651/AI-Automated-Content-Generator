from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap
import uuid

OUTPUT_DIR = Path("data/generated_images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def generate_instagram_image(
    text,
    size=(1080, 1080),
    bg_color=(15, 15, 15),
    text_color=(255, 255, 255)
):
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)

    # Use a bold font (change path if needed)
    font_path = "assets/fonts/Montserrat-Bold.ttf"
    font = ImageFont.truetype(font_path, 64)

    # Wrap text
    wrapped_text = textwrap.fill(text, width=18)

    # Calculate position
    bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (size[0] - text_width) // 2
    y = (size[1] - text_height) // 2

    draw.multiline_text(
        (x, y),
        wrapped_text,
        font=font,
        fill=text_color,
        align="center"
    )

    filename = OUTPUT_DIR / f"insta_{uuid.uuid4().hex}.png"
    img.save(filename)

    return str(filename)
