import sys
import requests
import json
import re

import argparse

from datetime import datetime


URL = "https://quake.360.net/api/v3/search/quake_service"
header = {
    "Content-Type": "application/json",
    "X-QuakeToken": "your_token_here",
}


args = argparse.ArgumentParser(description="Quake API in python", formatter_class=argparse.RawTextHelpFormatter)

args.add_argument("-q", "--query", help="Query to search")
args.add_argument("-o", "--output", choices=["txt", "json", "all"], help="Output format")
args.add_argument("-st", "--start-time", help="Start time of the query, format YYYY-mm-dd HH:MM:SS UTC")
args.add_argument("-et", "--end-time", help="End time of the query, format YYYY-mm-dd HH:MM:SS UTC")


def init_header():
    _conf_file = "quake.conf"
    try:
        config = {}
        with open(_conf_file, "r") as file:
            for line in file.readlines():
                conf = line.split(":")
                k = conf[0].strip()
                v = conf[1].strip()
                config.update({k: v})
        return config
    except FileNotFoundError as e:
        print(e)
        print(f"\nCreating {_conf_file}")
        with open(_conf_file, "w") as file:
            file.write("X-QuakeToken: <your-token-here>\nsize: <number-of-results>")
        msg = ("Please provide following information in the file:\n"
              "X-QuakeToken: <your-token-here>\n"
              "size: <number-of-results>")
        print(msg)
        sys.exit(1)


def datetime_qualifier(date_str):
    formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return True
        except ValueError:
            continue
    print(f"Invalid datetime format: {date_str}")
    return False


def update_time_param(time, key, data):
    if time:
        if datetime_qualifier(time):
            data.update({key: time})
        else:
            print(f"Invalid {key} format, {key} will not be added")


def quake_query(query, start_time, end_time, header=init_header()) -> list:
    data = {
        "query": query,
        "start": 0,
        "size": header.get("size"),
        "latest": True
    }
    update_time_param(start_time, "start_time", data)
    update_time_param(end_time, "end_time", data)
    del header["size"]

    resp = requests.post(URL, headers=header, json=data)
    resp = resp.json()

    if resp.get("code") == 0: # succeed query
        return resp.get("data")
    else:
        error_data = {
            "code": resp.get("code"),
            "message": resp.get("message")
        }
        print(error_data)
        sys.exit(1)


def out_to_txt(data, file_name):
    with open(file_name, "w") as f:
        for d in data:
            ip_port = f"{d.get('ip')}:{d.get('port')}"
            domain_port = f" {d.get('domain')}:{d.get('port')}" if d.get("domain") else " None"
            time = f" {d.get('time')}\n"
            f.write(ip_port + domain_port + time)


def out_to_json(data, file_name):
    values = [
        {
            "ip": d.get("ip"),
            "port": d.get("port"),
            "domain": d.get("domain") if d.get("domain") else "None",
            "time": d.get("time")
        }
        for d in data
    ]

    with open(file_name, "w") as f:
        json.dump(values, f, indent=4)


def result_summary(result_num, start_time, end_time):
    duration = (end_time - start_time).total_seconds()
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    milliseconds = int((duration * 1000) % 1000)
    result_str = f"\n[INFO] Total {result_num} result found in"
    result_str += f" {hours} hours" if hours else ""
    result_str += f" {minutes} minutes" if minutes else ""
    result_str += f" {seconds} seconds" if seconds else ""
    result_str += f" {milliseconds} milliseconds" if milliseconds else ""
    return result_str


def main(args):
    starting = datetime.now()

    resp_data = None
    if args.query:
        resp_data = quake_query(args.query, args.start_time, args.end_time)

    ending = datetime.now()
    result_num = len(resp_data)

    if resp_data:
        # print to stdout
        for data in resp_data:
            print(f"{data.get('ip')}:{data.get('port')}", end="")
            if data.get("domain"):
                print(f" {data.get('domain')}:{data.get('port')}", end="")
            else:
                print(" None", end="")
            print(f" {data.get('time')}")

        # --output
        out_name_prefix = re.sub(r":[ ]*| ", "_", args.query)
        if args.output == "txt":
            # output to txt
            out_to_txt(resp_data, f"{out_name_prefix}.txt")
        elif args.output == "json":
            # output to json
            out_to_json(resp_data, f"{out_name_prefix}.json")
        elif args.output == "all":
            # output to both
            out_to_txt(resp_data, f"{out_name_prefix}.txt")
            out_to_json(resp_data, f"{out_name_prefix}.json")

    print(result_summary(result_num, starting, ending))

if __name__ == "__main__":
    args = args.parse_args()
    main(args)

