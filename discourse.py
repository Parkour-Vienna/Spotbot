import logging
import urllib

import requests


class Forum(object):
    def __init__(self, url, username, key):
        self.url = url
        self.username = username
        self.key = key
        self.header = {
            'Api-Username': username,
            'Api-Key': key,
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def check_connection(self):
        resp = requests.get(url=self.url + '/categories.json', headers=self.header)
        if not resp.status_code == 200:
            raise ConnectionError(f'Server responded with status code {resp.status_code} {resp}')
        if not resp.json()['category_list']['can_create_topic']:
            raise ConnectionError('Api Key does not have enough permissions')
        logging.info('connection check successful')

    def create_topic(self, category_id, title, content, event=None):
        data = {
            'title': title,
            'category': category_id,
            'raw': content,
        }
        if event is not None:
            data['event'] = event
        return self._post('/posts.json', data)

    def create_post(self, topic_id, content):
        data = {
            'topic_id': topic_id,
            'raw': content
        }
        return self._post('/posts.json', data=data)

    def edit_post(self, post_id, new_content):
        data = {
            'post': {
                'raw': new_content,
            }
        }
        return self._put(f'/posts/{post_id}.json', data)

    def get_posts(self, topic_id):
        return self._get(f'/t/{topic_id}.json')['post_stream']['posts']

    def make_banner(self, topic_id):
        self._put(f'/t/{topic_id}/make-banner')

    def remove_banner(self, topic_id):
        self._put(f'/t/{topic_id}/remove-banner')

    def change_topic_status(self, topic_id, status, enabled):
        data = {
            'status': status,
            'enabled': enabled,
        }
        self._put(f'/t/{topic_id}/status', data)

    def delete_topic(self, topic_id):
        resp = requests.delete(f'{self.url}/t/{topic_id}.json', headers=self.header)
        if resp.status_code != 200:
            raise ConnectionError(f'Server responded with status code {resp.status_code}')

    def search_topic(self, title):
        logging.info(f'searching for existing topic with title: {title}')
        results = self._get(f'/search/query?term={urllib.parse.quote(title)}')
        if 'topics' not in results:
            return None
        for topic in results['topics']:
            logging.info(f'found topic with title {topic["title"]}')
            if topic['title'] == title:
                return topic
        return None

    def close_topic(self, topic_id):
        self._put(f'/t/{topic_id}/status', {'status': 'closed', 'enabled': 'true'})

    def _put(self, url, data={}):
        resp = requests.put(url=self.url + url, headers=self.header, json=data)
        if not resp.status_code == 200:
            raise ConnectionError(f'Server responded with status code {resp.status_code} {resp.text}')
        return resp

    def _post(self, url, data):
        resp = requests.post(url=self.url + url, headers=self.header, json=data)
        if not resp.status_code == 200:
            raise ConnectionError(f'Server responded with status code {resp.status_code}')
        return resp.json()

    def _get(self, url):
        resp = requests.get(url=self.url + url, headers=self.header)
        if not resp.status_code == 200:
            raise ConnectionError(f'Server responded with status code {resp.status_code}')
        return resp.json()
