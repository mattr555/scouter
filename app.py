from flask import Flask, render_template
from flask.ext.bower import Bower
from models import db, Team, Event, SkillResult, Match
from operator import attrgetter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/data.db'
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
