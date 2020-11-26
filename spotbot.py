import datetime
import json
import os

from discourse import Forum
from trainings import Tuesday


class Spotbot(object):
    def __init__(self, forum: Forum, savefile):
        self.forum = forum
        self.savefile = savefile
        if os.path.isfile(savefile):
            with open(savefile) as f:
                saved = json.load(f)
                self.tuesday = Tuesday(saved['tuesday_thread'], saved['tuesday_post'], saved['tuesday_created'],
                                       saved['tuesday_decided'])

    def run(self):
        now = datetime.datetime.now()
        if now.weekday() == 3:  # Tuesday
            if not self.tuesday.decision_made:
                spot = self.find_spotdecision(self.tuesday.thread_id)
                if spot is not None:
                    self.make_decision(self.tuesday, self.tuesday.spotdecision_str(spot))
                    self.tuesday.decision_made = True
            if now.hour == 23:
                if self.tuesday.thread_created != now.today().strftime('%d.%m.%Y'):
                    self.create_thread(self.tuesday)
                    self.tuesday.decision_made = False
                    self.save()

    def find_spotdecision(self, thread_id):
        posts = [x['cooked'] for x in self.forum.get_posts(thread_id)]
        for p in posts:
            if any(x in p.lower() for x in ['spot-decision:', 'spot decision:', 'decision:']):
                return p
        return None

    def make_decision(self, training, content):
        self.forum.edit_post(training.post_id, content)
        self.forum.make_banner(training.thread_id)

    def create_thread(self, training):
        self.forum.remove_banner(training.thread_id)
        self.forum.change_topic_status(training.thread_id, 'pinned_globally', False)

        date_str = (datetime.date.today() + datetime.timedelta(weeks=1)).strftime('%d.%m.%Y')
        resp = self.forum.create_topic(5, training.title(date_str), training.initial_post_str())
        training.thread_id = resp['topic_id']
        training.post_id = resp['id']
        training.thread_created = datetime.date.today().strftime('%d.%m.%Y')
        self.forum.change_topic_status(training.thread_id, 'pinned_globally', True)
        print(f'Neuer Thread für {training.title(date_str)} erstellt')

    def save(self):
        with open(self.savefile, 'w') as f:
            json.dump({
                'tuesday_thread': self.tuesday.thread_id,
                'tuesday_post': self.tuesday.post_id,
                'tuesday_created': self.tuesday.thread_created,
                'tuesday_decided': self.tuesday.decision_made
            }, f)
