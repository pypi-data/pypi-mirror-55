from os import environ

from ckan import plugins

from ckan.config import environment

CONFIG_FROM_HEROKU_ENV_VARS = {
    'sqlalchemy.url': 'DATABASE_URL',
    'ckan.datastore.write_url': 'HEROKU_POSTGRESQL_PINK_URL',
    'ckan.datastore.read_url': 'HEROKU_POSTGRESQL_GREEN_URL',
    # 'ckan.redis.url': 'CKAN_REDIS_URL',
    # 'solr_url': 'CKAN_SOLR_URL',
    # 'solr_user': 'CKAN_SOLR_USER',
    # 'solr_password': 'CKAN_SOLR_PASSWORD',
    # 'ckan.site_id': 'CKAN_SITE_ID',
    # 'ckan.site_url': 'CKAN_SITE_URL',
    # 'ckan.storage_path': 'CKAN_STORAGE_PATH',
    # 'ckan.datapusher.url': 'CKAN_DATAPUSHER_URL',
    # 'smtp.server': 'CKAN_SMTP_SERVER',
    # 'smtp.starttls': 'CKAN_SMTP_STARTTLS',
    # 'smtp.user': 'CKAN_SMTP_USER',
    # 'smtp.password': 'CKAN_SMTP_PASSWORD',
    # 'smtp.mail_from': 'CKAN_SMTP_MAIL_FROM',
    # 'ckan.max_resource_size': 'CKAN_MAX_UPLOAD_SIZE_MB',
}


class HerokuPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    def update_config(self, config):
        for option, env in CONFIG_FROM_HEROKU_ENV_VARS.items():
            value = environ.get(env)

            if value:
                config[option] = value
