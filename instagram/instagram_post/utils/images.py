import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random


def download_image(image_url: str) -> Image:
    """
    Downloads an image from the specified URL and converts it to RGB format.

    :param image_url: URL of the image to download.
    :return: Image object in RGB format.
    """
    response = requests.get(image_url)
    response.raise_for_status()
    image_data = BytesIO(response.content)

    image = Image.open(image_data)
    image = image.convert('RGB')
    return image

def add_text_to_image(canvas: Image, text: str, position: tuple, font_size: int = 60, anchor: str = 'lm') -> Image:
    """
    Adds text to the provided canvas at the specified position.

    :param canvas: The image canvas where text will be added.
    :param text: The text to add.
    :param position: The position (x, y) where the text will be placed.
    :param font_size: Font size of the text.
    :param anchor: Anchor for the text placement.
    :return: The image canvas with the added text.
    """
    draw = ImageDraw.Draw(canvas)
    font_path = '../resources/fonts/Oswald-VariableFont_wght.ttf'
    font = ImageFont.truetype(font_path, font_size)

    wrapped_text = textwrap.fill(text, width=20)
    text_x, text_y = position

    draw.text((text_x, text_y), wrapped_text, font=font, fill=(255, 255, 255), align="left", anchor=anchor)
    return canvas

def create_image_with_title(title: str, image_url: str) -> None:
    """
    Creates an image with a title overlaid on a background, combining two images.

    :param title: The title text to overlay on the image.
    :param image_url: URL of the image to download and use as a base.
    """
    base_image = download_image(image_url)

    width, height = base_image.size
    min_dim = min(width, height)  # La dimensión mínima para el recorte cuadrado
    left = (width - min_dim) // 2
    top = (height - min_dim) // 2
    right = (width + min_dim) // 2
    bottom = (height + min_dim) // 2

    base_image = base_image.crop((left, top, right, bottom))
    base_image = base_image.resize((415,415))

    canvas_size = (1000, 1000)
    canvas = Image.new('RGB', canvas_size, (0, 0, 0))

    base_image_width, base_image_height = base_image.size
    x_offset = ((canvas_size[0] - base_image_width) // 2) + int(canvas_size[0] * 0.27)
    y_offset = (canvas_size[1] - base_image_height) // 2  + int(canvas_size[1]*0.22)
    canvas.paste(base_image, (x_offset, y_offset))

    overlay_image = Image.open('../resources/images_templates/1.png')
    overlay_image.thumbnail(canvas_size, Image.LANCZOS)

    overlay_width, overlay_height = overlay_image.size
    overlay_x = (canvas_size[0] - overlay_width) // 2
    overlay_y = (canvas_size[1] - overlay_height) // 2
    canvas.paste(overlay_image, (overlay_x, overlay_y), overlay_image)

    canvas = add_text_to_image(canvas, title, position=(70, 450))
    return canvas


def create_slide_with_text(text: str, canvas_size: tuple = (1000, 1000)) -> None:
    """
    Create a slide with the given text overlayed on a randomly chosen image.

    :text (str): The text to overlay on the image.
    :canvas_size (tuple, optional): The size of the canvas for the image. Defaults to (1000, 1000).
    """

    image_number = random.choice([2, 5])
    image_path = f'../resources/images_templates/{image_number}.png'

    image = Image.open(image_path)
    image.thumbnail(canvas_size, Image.LANCZOS)
    canvas = add_text_to_image(image, text, position=(500, 500), font_size=60, anchor='mm')

    return canvas
