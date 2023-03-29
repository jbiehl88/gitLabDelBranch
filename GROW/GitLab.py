import gitlab
import os
import datetime
from dotenv import load_dotenv
from dateutil.parser import parse

# Requires an .env file with ACCESS_TOKEN = 'GitLab Personal Access Token'
load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

# Connection to GitLab with above Token
gl = gitlab.Gitlab("https://gitlab.com/", ACCESS_TOKEN)

# Current date & time (UTC)
now = datetime.datetime.now().astimezone(datetime.timezone.utc)

# Change the number of days to adjust how old the branches need are to be deleted
THRESHOLD = now - datetime.timedelta(days=7)

# Iterates through all groups and all projects and verifies if the branches are over a certain
# age and deletes them if they are over that date (does not delete the main/master branch.
def del_branches():
    for project in gl.projects.list(owned=True):
        for branch in project.branches.list(owned=True):
            commit = branch.commit
            date = parse(commit['committed_date'])
            if date < THRESHOLD and branch.name != "main" and branch.name != "master":
                branch.delete()


def main_del():
    del_branches()


main_del()
