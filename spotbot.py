import datetime
import json
import os
import logging

from discourse import Forum
from trainings import Training, Tuesdayness, ForumMeeting


class Spotbot(object):
    def __init__(self, forum: Forum):
        self.forum = forum

    def run(self):
        now = datetime.datetime.now()
        logging.info(f'running spotbot at {now}')

        today = datetime.datetime.now()
        nt = Spotbot._next_weekday(today, 4)
        lt = Spotbot._last_weekday(today, 4)
        logging.info(f'next tuesday will be {nt}')
        logging.info(f'last tuesday was {lt}')
        nfm = Spotbot._next_weekday(today, 6)
        lfm = Spotbot._last_weekday(today, 6)
        logging.info(f'next fm will be {nfm}')
        logging.info(f'last fm was {lfm}')

        trainings = [
            Tuesdayness(lt),
            Tuesdayness(nt),
            ForumMeeting(lfm),
            ForumMeeting(nfm),
        ]

        for t in trainings:
            self.reconcile(t)

        self.pin_banner(trainings)


    def _next_weekday(d, weekday):
        days_ahead = weekday - d.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return d + datetime.timedelta(days_ahead)

    def _last_weekday(d, weekday):
        delta = d.weekday() - weekday
        return d - datetime.timedelta(delta)

    def pin_banner(self, trainings):
        today = datetime.date.today()
        ordered = sorted(trainings, key=lambda t: t.date)
        filtered = list(filter(lambda t: t.date.date() >= today, ordered))
        next = filtered[0]
        logging.info(f'next training is {next.title()}')
        topic = self.forum.search_topic(next.title())
        if topic is None:
            raise 'could not find topic for banner'
        self.forum.make_banner(topic['id'])

    def reconcile(self, training: Training):
        topic = self.forum.search_topic(training.title())
        if topic is None:
            self.create_thread(training)
            self.reconcile(training)
            return

        topic_id = topic['id']
        logging.info(f'found topic with id {topic_id}')
        logging.debug(f'topic {topic}')

        if training.decision_time() > datetime.datetime.now():
            logging.info('decison time not yet reached')
            return
        if topic['closed']:
            logging.info('decision has already been made')
            return
        logging.info('posting decision')
        decision = self.find_spotdecision(topic_id)
        if decision is None:
            logging.warn('decision should be made but not decison could be found')
            return
        logging.info(f'found decision "{decision}"')
        posts = self.forum.get_posts(topic_id)
        self.forum.edit_post(posts[0]['id'], training.spotdecision_str(decision))
        self.forum.close_topic(topic_id)

    def find_spotdecision(self, thread_id):
        posts = [x['cooked'] for x in self.forum.get_posts(thread_id)]
        for p in posts:
            if any(x in p.lower() for x in ['spot-decision:', 'spot decision:', 'decision:']):
                return p
        return None

    def create_thread(self, training):
        # self.forum.remove_banner(training.thread_id)
        # self.forum.change_topic_status(training.thread_id, 'pinned_globally', False)

        resp = self.forum.create_topic(5, training.title(), training.initial_post_str())
        # self.forum.change_topic_status(training.thread_id, 'pinned_globally', True)
        logging.info(f'created thread for {training.title()}')
        return resp
