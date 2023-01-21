# scrap-badges

## about

Use [scrapy](https://scrapy.org/) to scrap Credily badges and output them in a README file.

## usage

```bash
pipenv install
BADGE_URL="www.credily.com/users/foobar/badges" README_PATH="./README.md" pipenv run python crawl.py
```
