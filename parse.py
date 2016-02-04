from app import app, db, Team, Event, SkillResult, Match
import click, csv, os, requests, bs4

db.app = app

def get_team(license, name=None):
	if not license:
		return
	t = Team.query.filter_by(license=license).first()
	if t:
		return t
	t = Team(license, name)
	db.session.add(t)
	return t


@click.group()
def cli():
	"""Download and parse data from robotevents.org"""

address = 'http://ajax.robotevents.com/tm/results/{}/?format=csv&sku={}&div=1'

@cli.command('download')
@click.argument('sku')
@click.argument('name')
def download_event(sku, name):
	"""Download event data"""
	to_dl = os.path.join(os.path.dirname(__file__), 'data', name)
	os.mkdir(to_dl)
	click.echo('downloading {} to {}'.format(sku, to_dl))
	for file in ['matches', 'rankings', 'skills_programming', 'skills_robot']:
		r = requests.get(address.format(file, sku)).content
		with open(os.path.join(to_dl, file+'.csv'), 'w') as f:
			f.write(r)

@cli.command('clean')
def clean():
	"""clean the database out"""
	click.echo('destroying db...')
	db.drop_all()
	db.create_all()
	click.echo('done')

@cli.command('parse')
@click.argument('names', nargs=-1)
@click.pass_context
def parse_event(ctx, names):
	"""Parse event named NAME"""
	if names == ('all',) or not names:
		ctx.invoke(clean)
		names = set(os.listdir('data')) - set(['data.db'])
	for name in names:
		click.echo('parsing {}'.format(name))
		path = os.path.join(os.path.dirname(__file__), 'data', name)
		rankings_fn = os.path.join(path, 'rankings.csv')
		rankings = csv.DictReader(open(rankings_fn))
		teams = []
		for row in rankings:
			teams.append(get_team(row['teamnum'], row['teamname']))
			sku = row['sku']
		event = Event(name=name, teams=teams, sku=sku)
		db.session.add(event)

		for i, skill_type in enumerate(['robot', 'programming']):
			fn = os.path.join(path, 'skills_{}.csv'.format(skill_type))
			reader = csv.DictReader(open(fn))
			for row in reader:
				res = SkillResult(type=i, score=int(row['highscore']), team=get_team(row['team']), event=event)
				db.session.add(res)

		fn = os.path.join(path, 'matches.csv')
		reader = csv.DictReader(open(fn))
		for row in reader:
			m = Match()
			m.name = name + '.' + row['round'] + '.' + row['instance'] + '.' + row['matchnum']
			r = set(row[i] for i in ('red1', 'red2', 'red3')) - set([''])
			m.reds = [get_team(i) for i in r]
			b = set(row[i] for i in ('blue1', 'blue2', 'blue3')) - set([''])
			m.blues = [get_team(i) for i in b]
			m.red_score = int(row['redscore'])
			m.blue_score = int(row['bluescore'])
			m.event = event
			db.session.add(m)

		db.session.commit()
		click.echo('done')

team_list_address = 'http://www.robotevents.com/{}.html'

@cli.command('new')
@click.argument('sku')
@click.argument('name')
def new_event(name, sku):
	"""create a new upcoming event from a team list"""
	click.echo('parsing {} team list into {}'.format(sku, name))
	r = requests.get(team_list_address.format(sku)).text
	t = bs4.BeautifulSoup(r, 'html.parser')
	rows = t.find(id='reTeamTable').contents[3:]
	teams = []
	for row in rows:
		if type(row) is bs4.element.Tag:
			teams.append(get_team(row.contents[1].contents[0]))
	e = Event(name=name, teams=teams, sku=sku)
	db.session.add(e)
	db.session.commit()
	click.echo('done')

if __name__ == "__main__":
	cli()
