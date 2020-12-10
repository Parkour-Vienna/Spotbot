import pytz


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
        return '<p>Dies ist der wöchentliche Thread um für die Tuesdayness abzustimmen.' \
               'Ein paar Stunden vor dem Training werden die Stimmen zusammengezählt und der Spot entschieden.' \
               '<br><a href="...">Genauere Infos zur Tuesdayness</a></p>'

    def spotdecision_str(self, spot_decision):
        return spot_decision + '<br>Weitere Infos zur Tuesdayness findest du <a href="...">hier!</a>'

    def decision_time(self):
        return self.date.replace(hour=15, minute=0, second=0, microsecond=0)

    def event_date(self):
        return self.date.replace(hour=18, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)


class ForumMeeting(Training):
    def __init__(self, date):
        super().__init__(date)

    def title(self):
        return 'Forum Meeting am ' + self.date.strftime('%d.%m.%Y')

    def initial_post_str(self):
        return '<p>Dies ist der wöchentliche Thread für das Forum Meeting.' \
               'Ein paar Stunden vor dem Training werden die Stimmen zusammengezählt und der Spot entschieden.' \
               '<br><a href="...">Genauere Infos zum Forum Meeting</a></p>'

    def spotdecision_str(self, spot_decision):
        return spot_decision + '<br>Weitere Infos zum Forum Meeting findest du <a href="...">hier!</a>'

    def decision_time(self):
        return self.date.replace(hour=12, minute=0, second=0, microsecond=0)

    def event_date(self):
        return self.date.replace(hour=12, minute=0, second=0, microsecond=0, tzinfo=pytz.UTC)
