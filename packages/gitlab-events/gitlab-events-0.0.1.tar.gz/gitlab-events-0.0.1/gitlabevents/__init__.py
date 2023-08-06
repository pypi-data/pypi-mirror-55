from colorama import init
from gitlabevents.log import *
from gitlabevents.args import get_args

args = get_args()
token = args.token
path = args.output
server = args.server

log = Logger()


