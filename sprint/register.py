import requests
import os, json
from tabulate import tabulate
from utils import log, apply_auth_creds
from utils import save_slug, get_slug
from utils import process_action

def register(**kwargs):
    from constants import VERBOSE_COLOR_MAP
    from constants import VerbosityLevel
    from team import handle_team_reg

    data = get_slug()
    if data:
        sprint_slug = data['sprint_slug']
    else:
        return
    url = '{sprint_slug}' +  '/register/'
    resp = process_action(url, sprint_slug)

    if resp.status_code == 200:
        r_json = resp.json()
        is_team = r_json['team']
        if not is_team:
            handle_team_reg()
        else:
            msg = '{color}' + r_json['message'] + '{default_color}'
            msg_ctx = {'color':
                    VERBOSE_COLOR_MAP[r_json['verbosity_level']]}
            log(msg, msg_ctx)
    else:
        r_json = resp.json()
        msg = '{color}' + r_json['emessage'] + '{default_color}'
        msg_ctx = {'color': VERBOSE_COLOR_MAP[VerbosityLevel.ERROR]}
        log(msg, msg_ctx)


def access(**kwargs):
    from constants import VERBOSE_COLOR_MAP
    from constants import VerbosityLevel

    sprint_slug = kwargs['subcommand']
    url = '{sprint_slug}' +  '/access/'
    resp = process_action(url, sprint_slug)

    if resp.status_code == 200:
        r_json = resp.json()
        save_slug(sprint_slug)
        headers = []
        table = []

        row = []
        msg = '{color}'+'Hackathon Title'+'{default_color}'
        msg = msg.format(color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
                default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
        )
        row.append(msg)
        row.append(r_json['title'])
        table.append(row)

        row = []
        msg = '{color}'+'Short Description'+'{default_color}'
        msg = msg.format(color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
                default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
        )
        row.append(msg)
        row.append(r_json['short_description'])
        table.append(row)

        row = []
        msg = '{color}'+'URL'+'{default_color}'
        msg = msg.format(color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
                default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
        )
        row.append(msg)
        row.append(r_json['url'])
        table.append(row)

        row = []
        msg = '{color}'+'Start'+'{default_color}'
        msg = msg.format(color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
                default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
        )
        row.append(msg)
        row.append(r_json['start'])
        table.append(row)

        row = []
        msg = '{color}'+'End'+'{default_color}'
        msg = msg.format(color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
                default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
        )
        row.append(msg)
        row.append(r_json['end'])
        table.append(row)

        row = []
        msg = '{color}'+'Team Size'+'{default_color}'
        msg = msg.format(color=VERBOSE_COLOR_MAP[VerbosityLevel.BOLD],
                default_color=VERBOSE_COLOR_MAP[VerbosityLevel.INFO]
        )
        row.append(msg)
        row.append(r_json['team_size'])
        table.append(row)

        print tabulate(table, headers, tablefmt="grid")
    else:
        r_json = resp.json()
        msg = '{color}' + r_json['emessage'] + '{default_color}'
        msg_ctx = {'color': VERBOSE_COLOR_MAP[VerbosityLevel.ERROR]}
        log(msg, msg_ctx)