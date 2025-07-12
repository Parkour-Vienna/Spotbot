import pytz

ev = pytz.timezone('Europe/Vienna')

class Training(object):
    def __init__(self, date):
        self.date = date

    def title(self):
        return 'Thread Titel mit Datum ' + self.date.strftime('%d.%m.%Y')

    def initial_post_str(self):
        return 'Dieser Text wird gepostet wenn der Thread eröffnet wird'

    def spotdecision_str(self, spot_decision):
        return f'Dieser Text wird gepostet wenn die {spot_decision} feststeht'

    def decision_time(self):
        return self.date

    def event_date(self):
        return self.date.replace(tzinfo=pytz.UTC)


class Tuesdayness(Training):
    def __init__(self, date):
        super().__init__(date)

    def title(self):
        return 'Tuesdayness am ' + self.date.strftime('%d.%m.%Y')

    def initial_post_str(self):
        return '<p>Hier ist der wöchentliche Thread um für die Tuesdayness abzustimmen.<br>' \
               'Ein paar Stunden vor dem Training werden die Stimmen zusammengezählt und der Spot entschieden.' \
               '<br><a href="https://parkour.wien/t/was-ist-die-tuesdayness/1084">Mehr Infos zur Tuesdayness</a></p>'

    def spotdecision_str(self, spot_decision):
        return spot_decision + '<br>Weitere Infos zur Tuesdayness findest du <a href="https://parkour.wien/t/was-ist-die-tuesdayness/1084">hier!</a>'

    def decision_time(self):
        return ev.localize(self.date.replace(hour=15, minute=0, second=0, microsecond=0,tzinfo=None))

    def event_date(self):
        return ev.localize(self.date.replace(hour=19, minute=0, second=0, microsecond=0,tzinfo=None))


class ForumMeeting(Training):
    def __init__(self, date):
        super().__init__(date)

    def title(self):
        return 'Forum Meeting am ' + self.date.strftime('%d.%m.%Y')

    def initial_post_str(self):
        header = '<p>Hier ist der wöchentliche Thread für das Forum Meeting.<br>' \
                 'Die hier abgegebenen Stimmen werden bei der Entscheidung am Schwedenplatz berücksichtigt.<br>\n'
        extra = ''
        trailer = '\n<a href="https://parkour.wien/t/forum-meeting-informationen/24">Mehr Infos zum Forum Meeting</a></p>'
        extra = '\n> Bei diesem Training findet ein geleiteter Beginner-Workshop statt!\n'
        return header + extra + trailer

    def spotdecision_str(self, spot_decision):
        return spot_decision + '<br>Weitere Infos zum Forum Meeting findest du <a href="https://parkour.wien/t/forum-meeting-informationen/24">hier!</a>'

    def decision_time(self):
        return ev.localize(self.date.replace(hour=13, minute=0, second=0, microsecond=0,tzinfo=None))

    def event_date(self):
        return ev.localize(self.date.replace(hour=13, minute=0, second=0, microsecond=0,tzinfo=None))
