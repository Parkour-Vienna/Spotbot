class Training(object):
    def __init__(self, thread_id, post_id, created, decided):
        self.thread_id = thread_id
        self.post_id = post_id
        self.thread_created = created
        self.decision_made = decided

    def title(self, date):
        return 'Thread Titel mit Datum ' + date

    def initial_post_str(self):
        return 'Dieser Text wird gepostet wenn der Thread eröffnet wird'

    def spotdecision_str(self, spot_decision):
        return f'Dieser Text wird gepostet wenn die {spot_decision} feststeht'


class Tuesday(Training):
    def __init__(self, thread_id, post_id, created, decided):
        super().__init__(thread_id, post_id, created, decided)

    def title(self, date):
        return 'Tuesdayness am ' + date

    def initial_post_str(self):
        return '<p>Dies ist der wöchentliche Thread um für die Tuesdayness abzustimmen.' \
               'Ein paar Stunden vor dem Training werden die Stimmen zusammengezählt und der Spot entschieden.' \
               '<br><a href="...">Genauere Infos zur Tuesdayness</a></p>'

    def spotdecision_str(self, spot_decision):
        return spot_decision + '<br>Weitere Infos zur Tuesdayness findest du <a href="...">hier!</a>'
