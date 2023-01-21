# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import re
import sys

import scrapy
from scrapy.crawler import CrawlerProcess

from badgeupdate.spiders.badgespider import BadgeSpider

begin_line = "<!-- CREDLY_BADGES_START -->"
end_line = "<!-- CREDLY_BADGES_END -->"
badges = []


class ItemCollectorPipeline:
    def process_item(self, item, spider):
        badge = item["badge_src"]
        badges.append(f"![alt text]({badge})")


process = CrawlerProcess(
    {
        "USER_AGENT": "scrapy",
        "LOG_LEVEL": "INFO",
        "ITEM_PIPELINES": {"__main__.ItemCollectorPipeline": 100},
    }
)

try:
    filename = os.environ["README_PATH"]
except KeyError:
    print("Please provide an input file")
    sys.exit(1)

process.crawl(BadgeSpider)
process.start()

badges_str = "\n".join(badges)
old_section = f"{begin_line}.*?{end_line}"
new_section = f"{begin_line}\n{badges_str}\n{end_line}"
print(f"Updating {filename}")
with open(filename, "r+") as fp:
    fcontent = fp.read()
    modified_fcontent = re.sub(old_section, new_section, fcontent, flags=re.S)
    fp.seek(0)
    fp.write(modified_fcontent)
    fp.truncate()
