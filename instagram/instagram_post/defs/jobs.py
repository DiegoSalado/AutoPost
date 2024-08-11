from dagster import AssetSelection, define_asset_job

post_job = define_asset_job(
    name='post_job',
    selection=AssetSelection.groups('create_post')
)