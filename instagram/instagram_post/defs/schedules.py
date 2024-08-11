from instagram_post.defs.jobs import post_job
from dagster import ScheduleDefinition


post_schedule = ScheduleDefinition(
    job=post_job,
    cron_schedule = "0 19 * * *"
)
