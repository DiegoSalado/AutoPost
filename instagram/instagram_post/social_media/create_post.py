from dagster import asset
from dagster import AssetExecutionContext
from instagram_post.utils import *
import random
from instagrapi import Client
from dotenv import load_dotenv
import os
from datetime import datetime


load_dotenv(dotenv_path=".env")

INSTAGRAM_USER = os.getenv("INSTAGRAM_USER")
INSTAGRAM_PASWORD = os.getenv("INSTAGRAM_PASWORD")
GROUP_NAME = "create_post"


@asset(group_name=GROUP_NAME)
def get_article(context: AssetExecutionContext):

    articles = fetch_spaceflight_articles()
    article = random.choice(articles['results'])
    article['html'] = extract_text_from_url(article['url'])

    context.log.info(article)
    return article
    

@asset(group_name=GROUP_NAME)
def create_content(context: AssetExecutionContext, get_article:dict):

    article = get_article

    while True:
        try:
            llm_response = generate_instagram_slides(article['title'], article['html'])
            context.log.info(llm_response)
            break
        except Exception as e:
            context.log.info(e)
            pass
        
    article['slides'] = llm_response

    context.log.info(article)
    return article
    

@asset(group_name=GROUP_NAME)
def create_images(context: AssetExecutionContext, create_content:dict):

    article = create_content
    date_str = datetime.now().strftime('%Y-%m-%d')
    image_folder = os.path.join('images', date_str)
    os.makedirs(image_folder, exist_ok=True)


    image_1 = create_image_with_title(article['slides'][f'slide_1'], article['image_url'])
    image_1 = image_1.convert('RGB')
    image_1.save(os.path.join(image_folder, 'image_1.jpg'))
    for i in range(2,6):
        image_i = create_slide_with_text(article['slides'][f'slide_{i}'])
        image_i = image_i.convert('RGB')
        image_name = os.path.join(image_folder, f'image_{i}.jpg')
        image_i.save(image_name)

    article['images'] = [os.path.join(image_folder, f'image_{x}.jpg') for x in range(1,6)]

    return article


@asset(group_name=GROUP_NAME)
def post_images(context: AssetExecutionContext, create_images:dict):

    article = create_images

    bot = Client()
    bot.login(INSTAGRAM_USER, INSTAGRAM_PASWORD)

    bot.album_upload(
        article['images'],
        article['slides']['description']
    )