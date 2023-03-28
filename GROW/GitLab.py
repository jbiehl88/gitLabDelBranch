import gitlab
import os
import datetime
from dotenv import load_dotenv
from dateutil.parser import parse

load_dotenv()
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

gl = gitlab.Gitlab("https://gitlab.com/", ACCESS_TOKEN)

now = datetime.datetime.now().astimezone(datetime.timezone.utc)
THRESHOLD = now - datetime.timedelta(days=7)


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
