#!/usr/bin/env python3

import datetime

import tabulate

from presidentsCTF import api, config, db, notify

"""
Display - tabulate and print the scoreboard locally.
"""

def to_display(t, active, is_active, is_known, is_top_n):
    """Check conditions to determine if the use wants to see this team"""
    if  is_top_n > 0 and t["rank"] <= is_top_n:
        return True
    if is_active and active:
        return True
    if is_known and t["name"] in config.config["teams"]:
        return True
    return False

def scoreboard(event_id, is_active, is_known, is_top_n, show_detailed):
    known = config.config["teams"]
    headers = ["Rank", "Team", "Score", "Solves", "Duration", "Remaining"]
    # add solves per points
    if show_detailed:
        bins = [b["points"] for b in db.event_points_bins(event_id)]
        headers += bins

    current_time = datetime.datetime.utcnow()
    event = db.event_by_id(event_id)
    teams = db.all_teams_by_rank(event_id)
    show = []
    for t in teams:
        row = [t[f] for f in ["rank", "name", "score", "solves"]]
        _, dur = api.parse_duration(t["duration"])
        row.append(dur)
        left, active = api.start_to_time_left(t["start"], current_time)
        row.append(left)
        if show_detailed:
            pts = {p["points"]: p["cnt"] for p in db.team_solve_durations(t["team_id"], event_id)}
            for score in bins:
                if score in pts:
                    row.append(pts[score])
                # has a multi-solve so will not add up
                elif t["solves"] != sum(pts.values()):
                    row.append("*")
                else:
                    row.append(0)
        if to_display(t, active, is_active, is_known, is_top_n):
            # update generic name to matching known name
            if t["name"] in known:
                row[1] = known[t["name"]]
            show.append(row)

    table = tabulate.tabulate(show, headers, tablefmt="github")
    table_sz = (table.index('\n'))
    blk = "#"*table_sz
    title = "{}\n{}\n{}\n".format(blk,event["name"],blk)
    print(title + table +"\n")

TOP_TEAM = "New leader! {} scored {} points and moves into 1st with {} total points."
NEW_SOLVE = "{} solved a challenge for {} points. Now ranked {} with {} points."
NEW_MULTI = "{} solved {} challenges for {} points. Now ranked {} with {} points."
DM_PREFIX = "<{}>: "
WATCH_DM = DM_PREFIX + "{} dropped {} places to {}."
def summarize_changes(changes, to_slack, to_twitter):
    known = config.config["teams"]
    watch = config.config["slack"]["watch"] if to_slack else {}
    advancement = []
    dm = []
    for team_id, change in changes.items():
        team = change["team"]
        if change["new"]:
            advancement.append((team, change))
        elif change["rank"] > 0:
            advancement.append((team, change))
        elif team["name"] in watch:
            dm.append((team, change))
        elif change["solves"] > 0:
            advancement.append((team, change))

    msgs = []

    # track solves/scoreboard changes
    now = datetime.datetime.utcnow()
    show = sorted(advancement, key=lambda x: x[0]["rank"])
    for (team,change) in show:
        (left, active) = api.start_to_time_left(team["start"], now)
        name, rank, score = [team[f] for f in ["name", "rank", "score"]]
        # swap in known team name
        if name in known:
            name = "{} ({})".format(known[name], name)
        solves, points, diff_rank = [change[f] for f in ["solves","points", "rank"]]
        # special message for new top team
        if rank == 1 and (diff_rank > 0 or change["new"]):
            msg = TOP_TEAM.format(name, points, score)
        elif solves == 1:
            msg = NEW_SOLVE.format(name, points, rank, score)
        elif solves > 1 :
            msg = NEW_MULTI.format(name, solves ,points, rank, score)
        else:
            logging.warn("unknown state: {} {}".format(team, chage))
            continue

        # add time remaining.
        msg += " {} remaining.".format(left) if active else " Final."

        # if the message is going to slack and it is a watched team, prefix it
        if to_slack and name in watch:
            msg = DM_PREFIX.format(watch[name]) + msg

        msgs.append(msg)

    # for teams where we want all the changes
    for (team, change) in dm:
        msg = WATCH_DM.format(team["name"], -change["rank"], team["rank"])
        msgs.append(msg)

    # header
    if len(msgs) > 0:
        print("Updates:")
    else:
        print("No updates.")

    # reverse order so most recent message talks about the top team
    msgs.reverse()
    for m in msgs:
        print(m)
    print()

    if to_slack:
        notify.send_slack_messages(msgs)

    if to_twitter:
        notify.send_twitter_messages(msgs)

