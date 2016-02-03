from flask import Flask, render_template, request
from flask.ext.bower import Bower
from models import db, Team, Event, SkillResult, Match, Tag
from operator import attrgetter
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////vagrant/data/data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
Bower(app)

@app.route('/')
def index():
    return render_template('blah.html', teams=sorted(sorted(Team.query.all(), key=attrgetter('license')), key=attrgetter('school')))

@app.route('/team/<license>')
def team(license):
    t = Team.query.filter_by(license=license).first_or_404()
    return render_template('team.html', team=t)

@app.route('/ajax/notes', methods=["POST"])
def update_notes():
    t = Team.query.filter_by(license=request.form['license']).first_or_404()
    t.notes = request.form['notes']
    db.session.add(t)
    db.session.commit()
    return t.notes

def get_tag(n):
    t = Tag.query.filter_by(name=n).first()
    if t:
        return t
    t = Tag(n)
    db.session.add(t)
    return t

@app.route('/ajax/tag', methods=["POST"])
def update_tag():
    tag = get_tag(request.form['name'])
    team = Team.query.filter_by(license=request.form['license']).first()
    if request.form['do'] == 'add':
        if tag not in team.tags:
            team.tags.append(tag)
    else:
        if tag in team.tags:
            team.tags.remove(tag)
    db.session.add(team)
    db.session.commit()
    return render_template('taglist.html', tags=team.tags, team=team)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
