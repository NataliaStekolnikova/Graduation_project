# tasks
from __future__ import absolute_import, unicode_literals
from celery import Celery
from celery import app, shared_task

# job model
from .models import News

# scraping
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# logging
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# save function
@shared_task(serializer='json')
def save_function(article_list):
    #source = article_list[0]['source']
    source = 'HackerNews RSS'
    new_count = 0

    error = True
    try:
        latest_article = News.objects.filter(source=source).order_by('-published')[0]
    except Exception as e:
        print('Exception at latest_article: ')
        print(e)
        error = False
        pass
    finally:
        # if the latest_article has an index out of range (nothing in model) it will fail
        # this catches failure so it passes the first if statement

        if error is not True:
            latest_article = None

    for article in article_list:

        # latest_article is None signifies empty DB
        if latest_article is None:
            try:
                News.objects.create(
                    title=article['title'],
                    link=article['link'],
                    published=article['published'],
                    source=article['source']
                )
                new_count += 1
            except Exception as e:
                print('failed at latest_article is none')
                print(e)
                break

        # latest_article.published date < article['published']
        # halts the save, to avoid repetitive DB calls on already existing articles
        elif latest_article.published < article['published']:
            try:
                News.objects.create(
                    title=article['title'],
                    link=article['link'],
                    published=article['published'],
                    source=article['source']
                )
                new_count += 1
            except:
                print('failed at latest_article.published = ', article['published'])
                break
        else:
            return print('no news to add')

    logger.info(f'New articles: {new_count} articles(s) added.')
    return print('finished')

# scraping function
@shared_task
def news_scraping():
    article_list = []

    try:
        print('Starting the scraping tool')
        # execute my request, parse the data using html.parser
        # parser in BS4
        r = requests.get('https://news.ycombinator.com/rss')
        soup = BeautifulSoup(r.content, 'html.parser')

        # select only the "items" from the RSS
        #  <item>
        #  <title>Ask HN: Any interesting books you have read lately?</title>
        #  <link/>https://news.ycombinator.com/item?id=37156372
        #  <pubdate>Thu, 17 Aug 2023 02:18:00 +0000</pubdate>
        #  <comments>https://news.ycombinator.com/item?id=37156372</comments>
        #  <description><![CDATA[<a href="https://news.ycombinator.com/item?id=37156372">Comments</a>]]></description>
        #  </item>
        articles = soup.findAll('item')

        # for each "item" I want, parse it into a list
        for a in articles:
            title_tag = a.find('title')
            if title_tag is not None:
                title = title_tag.text
            else:
                print("Title tag not found:", a)
                title = "No title available"

            link_tag = a.find('link')
            if link_tag is not None:
                link = link_tag.next_sibling
            else:
                print("Link tag not found:", a)
                link = "No link available"

            published_tag = a.find('pubdate')
            if published_tag is not None:
                published = datetime.strptime(published_tag.text, '%a, %d %b %Y %H:%M:%S %z')
            else:
                print("Published tag not found:", a)
                published = None

            article = {
                'title': title,
                'link': link,
                'published': published,
                'source': 'HackerNews RSS'
            }
            article_list.append(article)
        print(f'Finished scraping {len(article_list)} articles')
        return save_function(article_list)
    except Exception as e:
        print('The scraping job failed. See exception:')
        print(e)
