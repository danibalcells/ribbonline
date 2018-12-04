from datetime import datetime as dt



class Event(object):

    def __init__(self, date, description):
        self.date = date
        self.description = description

    def __str__(self):
        return f'{self.date_label}: {self.description}'

    def __repr__(self):
        return f'<Event "{self}">'

    @property
    def date_label(self):
        return self.date.strftime("%b %d, %Y")


class EventTimeline(object):

    def __init__(self, events):
        self.events = events

    def __iter__(self):
        for e in self.events:
            yield e

    @property
    def dates(self):
        return [e.date for e in self.events]

    @property
    def date_labels(self):
        return [e.date_label for e in self.events]

    @property
    def descriptions(self):
        return [e.description for e in self.events]

EVENTS = EventTimeline([
    Event(dt(2017, 9, 6), ('The regional parliament passes a bill '
                           'calling a self-determination referendum.')),
    Event(dt(2017, 9, 11), ('National Day of Catalonia. One million '
                             'people gather in a pro-independence rally '
                             'in Barcelona, according to local police.')),
    Event(dt(2017, 9, 20), ('Police search Generalitat and party headquarters '
                            'for evidence of the illegal referendum. 14 '
                            'arrested for taking part in its organization. '
                            'Thousands protest in Barcelona.')),
    Event(dt(2017, 10, 1), 'Catalan self-determination referendum.'),
    Event(dt(2017, 10, 3), ('General strike. 700,000 protestors gather in '
                            'Barcelona, according to local police. '
                            'King Philip VI addresses the nation.')),
    Event(dt(2017, 10, 10), ('The regional parliament declares independence, '
                             'only to suspend it immediately and call for '
                             'dialog.')),
    Event(dt(2017, 10, 12), ('National Day of Spain. 2,000 people gather '
                             'in a unionist rally in Barcelona, according '
                             'to local police.')),
    Event(dt(2017, 10, 27), ('The regional parliament declares independence. '
                             'The central government invokes Article 155, '
                             'dissolves the Generalitat and calls a regional '
                             'snap election.')),
    Event(dt(2017, 10, 29), ('300,000 people gather in a unionist rally '
                             'in Barcelona, according to local police. '
                             'Former regional president Carles Puigdemont '
                             'flees to Brussels.')),
    Event(dt(2017, 11, 2), ("Spain's National High Court sentences former "
                            "regional Vice-President and nine former "
                            "regional ministers to be held on remand pending "
                            "trial.")),
    Event(dt(2017, 11, 11), ("750,000 people, according to local police, "
                             "demand freedom for the jailed leaders "
                             "in Barcelona.")),
    Event(dt(2017, 12, 21), ("Regional election. The unionist Ciutadans party "
                             "earns the most seats. Separatist parties "
                             "preserve their majority.")),
    Event(dt(2018, 3, 23), ("Spain's Supreme Court charges Catalan political "
                            "leaders with rebellion. The former president "
                            "of the regional parliament and four regional "
                            "ministers are jailed pending trial.")),
    Event(dt(2018, 3, 25), ("Former regional president Carles Puigdemont "
                            "is arrested by German police.")),
    Event(dt(2018, 4, 5), ("German courts free Carles Puigdemont "
                           "on the grounds that the separatist movement "
                           "did not incur in violent acts, a requirement "
                           "for the crime of high treason in German law.")),
    Event(dt(2018, 5, 14), ("Quim Torra inaugurated as regional president.")),
    Event(dt(2018, 6, 1), ("Spanish Prime Minister Mariano Rajoy loses a "
                           "vote of no confidence. Pedro Sánchez, leader of "
                           "the Socialist Party, takes over.")),
    Event(dt(2018, 9, 11), ('National Day of Catalonia. One million '
                             'people gather in a pro-independence rally '
                             'in Barcelona, according to local police.')),
    Event(dt(2018, 10, 1), ('First anniversary of the self-determination '
                            'referendum. 180,000 people gather in Barcelona, '
                            'according to local police.')),
    Event(dt(2018, 10, 12), ('National Day of Spain.'))
])
