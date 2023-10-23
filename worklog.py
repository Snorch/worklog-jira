#!/usr/bin/python3
import os
import datetime
import sys, getopt
import requests
from requests.auth import HTTPBasicAuth
import json


config_file_path = "~/.config/worklog"

def print_help_and_exit(argv):
    print(f"{argv[0]} --issue <issue_id> \\\n"
          "  --comment <\"comment text\"> \\\n"
          "  --time <time> \\\n"
          "  [--server <server>] \\\n"
          "  [--email <email>] \\\n"
          "  [--token <token>] \\\n"
          f"--server, --token and --email can be read from {config_file_path} file\n")
    sys.exit()

def main(argv):
    issue = None
    comment = None
    time = None
    server = None
    email = None
    token = None

    opts, args = getopt.getopt(argv[1:],"hi:c:t:s:e:T:",["issue=", "comment=", "time=", "server=", "email=", "token="])
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print_help_and_exit(argv)
        if opt in ("-i", "--issue"):
            issue = arg
        if opt in ("-c", "--comment"):
            comment = arg
        if opt in ("-t", "--time"):
            time = arg
        if opt in ("-s", "--server"):
            server = arg
        if opt in ("-e", "--email"):
            email = arg
        if opt in ("-T", "--token"):
            token = arg

    if email == None or token == None or server == None:
        try:
            with open(os.path.expanduser(config_file_path)) as conf:
                data = json.load(conf)
                if "server" in data:
                    server = data["server"]
                if "email" in data:
                    email = data["email"]
                if "token" in data:
                    token = data["token"]
        except FileNotFoundError:
            print_help_and_exit(argv)

    if issue == None or comment == None or time == None or server == None  or email == None or token == None:
        print_help_and_exit(argv)

    headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
            }
    url = f"https://{server}/rest/api/3/issue/{issue}/worklog"
    auth = HTTPBasicAuth(email, token)
    payload = json.dumps( {
        "comment": {
            "content": [
                {
                    "content": [
                        {
                            "text": comment,
                            "type": "text"
                            }
                        ],
                    "type": "paragraph"
                    }
                ],
            "type": "doc",
            "version": 1
            },
        "started": datetime.datetime.now(datetime.timezone.utc).astimezone().strftime("%Y-%m-%dT%H:%M:%S.000%z"),
        "timeSpent": time
        } )

    response = requests.request(
            "POST",
            url,
            data=payload,
            headers=headers,
            auth=auth
            )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))


if __name__ == "__main__":
    main(sys.argv)
