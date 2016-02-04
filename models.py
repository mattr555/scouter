from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'))
)

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    license = db.Column(db.String, unique=True)
    long_name = db.Column(db.String)
    skill_results = db.relationship('SkillResult', backref='team', lazy='dynamic')
    tags = db.relationship('Tag', secondary=tags, backref=db.backref('teams', lazy='dynamic'))
    notes = db.Column(db.Text)

    def __init__(self, license, long_name):
        self.license = license
        self.long_name = long_name

    def __repr__(self):
        return '<Team {}>'.format(self.license)

    def best_skill(self, type):
        return self.skill_results.filter_by(type=type).order_by(-SkillResult.score).first()

    @property
    def school(self):
        if self.license.isdigit():
            return int(self.license)
        return int(self.license[:-1])

    @property
    def matches(self):
        return self.red_matches.union(self.blue_matches)

    @property
    def tag_list(self):
        return ', '.join([i.name for i in self.tags])


teamlist = db.Table('teamlist',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    sku = db.Column(db.String, unique=True)
    teams = db.relationship('Team', secondary=teamlist,
        backref=db.backref('events', lazy='dynamic'))
    matches = db.relationship('Match', backref='event')
    skill_results = db.relationship('SkillResult', backref='event')

    def __repr__(self):
        return '<Event {}: {} teams>'.format(self.name, len(self.teams))

reds = db.Table('reds',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'))
)

blues = db.Table('blues',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id')),
    db.Column('match_id', db.Integer, db.ForeignKey('match.id'))
)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    reds = db.relationship('Team', secondary=reds,
        backref=db.backref('red_matches', lazy='dynamic'))
    blues = db.relationship('Team', secondary=blues,
        backref=db.backref('blue_matches', lazy='dynamic'))
    red_score = db.Column(db.Integer)
    blue_score = db.Column(db.Integer)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    @property
    def SP(self):
        return min(self.red_score, self.blue_score)

    @property
    def winner(self):
        if self.red_score > self.blue_score:
            return "Red"
        elif self.red_score < self.blue_score:
            return "Blue"
        return "None"

    def score(self, license):
        if license in [i.license for i in self.reds]:
            return self.red_score
        elif license in [i.license for i in self.blues]:
            return self.blue_score
        return None

    def on_team(self, team, license):
        if team == "Red":
            return license in [i.license for i in self.reds]
        return license in [i.license for i in self.blues]

    def did_win(self, license):
        return self.score(license) != min(self.red_score, self.blue_score)

    def __repr__(self):
        return '<{}: {} {} - {} {}>'.format(
            self.name,
            ' '.join(i.license for i in self.reds),
            self.red_score, self.blue_score,
            ' '.join(i.license for i in self.blues))

class SkillResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer)
    score = db.Column(db.Integer)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))

    def __repr__(self):
        return '<{} score: {} at {} by {}>'.format(self.typename, self.score, self.event.name, self.team.license)

    @property
    def typename(self):
        return ['Driver', 'Programming'][self.type]

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)
