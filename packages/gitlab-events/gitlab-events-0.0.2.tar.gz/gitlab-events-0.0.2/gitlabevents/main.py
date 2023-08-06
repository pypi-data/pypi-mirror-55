import gitlab
import csv
import sys

from gitlabevents.log import Logger
from gitlabevents.args import get_args

log = Logger()
arg    = get_args()
server = arg.server
token  = arg.token
try:
    path   = arg.output
except:
    path   = sys.stdout.fileno()

def gl_auth(server, token):
    log.info("Connecting to %s..." % (server))
    gl = gitlab.Gitlab(server, private_token=token)
    try:
        gl.auth()
    except:
        log.failur("Connection refused")
        exit(-1)
    log.success("Auth complete")
    return gl
    
def clear_trash(event):
    """
    Clears needless keys from event dictionary
    """
    trash_list = [
        'author', 
        'push_data',
        'target_title',
        'target_type',
        'target_id',
        'target_iid',
        'note',
    ]
    for trash in trash_list:
        if trash in event.keys():
            del event[trash]

def push_values(table, projects):
    """
    Adds the list of values of each event for every project in projects
    """
    for project in projects:
        events = project.events.list()
        for event in events:
            event = event.attributes
            clear_trash(event)
            table.append([v for (k, v) in event.items()])

def main():
    gl = gl_auth(server, token)

    log.info("Fetching projects list")
    projects = gl.projects.list()

    log.info("Generating csv header")
    events = projects[0].events.list()
    event = events[0].attributes

    log.info("Clearing trash arguments")
    clear_trash(event)

    table = []
    table.append([k for k in event]) #adding header for result table
    push_values(table, projects)

    log.info("Wrinting result")
    with open(path, "w", newline="") as output:
        writer = csv.writer(output, delimiter=",")
        for line in table:
            writer.writerow(line)
    log.success("Done!")

