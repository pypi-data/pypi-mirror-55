#!/usr/bin/env python3

import argparse
import datetime
import json
import logging
import os

import tabulate

from presidentsCTF import config, db, api

def display_solve_durations(breakdown):
    rows = []
    for pts in breakdown:
        points, lo, avg, hi, count = [pts[f] for f in ["points","min", "avg", "max","cnt"]]
        rows.append((points,
            count,
            api.parse_duration(lo)[1],
            api.parse_duration(avg)[1],
            api.parse_duration(hi)[1]))
    headers = ["Points", "Solved", "Min", "Average", "Max"]
    table = tabulate.tabulate(rows, headers, tablefmt="github")
    brk = "#"*table.index('\n')
    print("\nSolve Breakdown (Hours:Minutes)\n"+brk)
    print(table)
    print(brk + "\n")

def event_stats(event):
    e_id = event["event_id"]
    title = "{} - {}".format(event["name"], e_id[:6])
    print(title)
    print("-"*len(title))
    print("Teams on scoreboard  : {}".format(len(db.all_teams_by_rank(e_id))))
    breakdown = db.event_solves(e_id)
    display_solve_durations(breakdown)


def team_stats(team_name):
    team = db.team_by_name(team_name)
    if team is None:
        print("No such team")
        return
    t_id, name, rank, score, solves, dur = [team[f] for f in ["team_id", "name", "rank", "score", "solves", "duration"]]

    headers = ["Rank", "Score", "Time"]
    row = [(rank, score, api.parse_duration(dur)[1])]
    table = tabulate.tabulate(row, headers, tablefmt="github")
    brk = "#"*table.index('\n')
    print(name + '\n' + brk)
    print(table)
    print(brk)

    # XXX: teams can be in more than one event, rework
    breakdown = db.team_solve_durations(t_id, team["event_id"])
    display_solve_durations(breakdown)


    solves = db.team_solves_for_event(t_id, team["event_id"])
    rows = []
    for n, s in enumerate(solves):
        pts, chals, dur = [s[f] for f in ["points", "chals", "duration"]]
        rows.append((n+1,
            pts if chals == 1 else "{} ({})".format(pts, chals),
            api.parse_duration(dur)[1]))

    headers = ["#", "Points", "Time (H:M)"]
    table = tabulate.tabulate(rows, headers, tablefmt="github")
    brk = "#"*table.index('\n')
    print("Solves in Order\n"+brk)
    print(table+'\n'+brk)


def process(args):
    # filter events to match request
    events = db.all_events()
    if args.event is not None:
        events = [e for e in events if args.event in e["event_id"]]

    if args.team is not None:
        team_stats(args.team)
    else:
        for e in events:
            event_stats(e)


def main():

    # setup arguments
    parser = argparse.ArgumentParser(description="President's CTF Stats")
    parser.add_argument('--config', help='config file to load from')
    parser.add_argument('--event', help='show event stats')
    parser.add_argument('--team', help='show team stats')
    args = parser.parse_args()


    # load configuration
    if args.config:
        config.load_config(args.config)
    else:
        config.load_config()

    # load db
    db_path = config.config["db"]
    db.load(db_path)


    process(args)

if __name__ == '__main__':
    main()
