from scrapy.commands import ScrapyCommand

from appNews.models import create_schema

class commands(ScrapyCommand):
    requires_project = True
    default_settings = {'LOG_ENABLE': False}

    def short_desc(self):
        return "Init database"

    def run(self, args, opts):
        print("Init database ...")
        create_schema()