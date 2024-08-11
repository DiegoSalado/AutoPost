from dagster import load_assets_from_modules

from instagram_post.social_media import (
    create_post
)

SOCIAL_MEDIA_MODULES = load_assets_from_modules([
    create_post
])