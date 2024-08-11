from dagster import Definitions

# from instagram_post import MODULES
from instagram_post.social_media import SOCIAL_MEDIA_MODULES

# # Import the jobs created
from instagram_post.defs import JOBS, SCHEDULES


defs = Definitions(
     assets=SOCIAL_MEDIA_MODULES
    , jobs=JOBS
    , schedules=SCHEDULES
)
