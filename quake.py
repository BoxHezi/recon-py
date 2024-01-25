import requests
import json
import re

import argparse


URL = "https://quake.360.net/api/v3/search/quake_service"
header = {
    "Content-Type": "application/json",
    "X-QuakeToken": "your_token_here",
}


args = argparse.ArgumentParser(description="Quake API in python", formatter_class=argparse.RawTextHelpFormatter)

args.add_argument("--query", "-q", help="Query to search")
args.add_argument("--output", "-o", choices=["txt", "json", "all"], help="Output format")
args.add_argument("--file", "-f", help="File to save the output")


def init_header():
    config = {}
    with open("quake.conf", "r") as file:
        for line in file.readlines():
            conf = line.split(":")
            k = conf[0].strip()
            v = conf[1].strip()
            config.update({k: v})
    return config


def quake_query(query, header=init_header()) -> list:
    data = {
        "query": query,
        "start": 0,
        "size": header.get("size"),
        "latest": True
    }
    del header["size"]

    resp = requests.post(URL, headers=header, json=data)
    try:
        return resp.json().get("data")
    except:
        return resp.json().get("message")


def out_to_txt(data, file_name):
    with open(file_name, "w") as f:
        for d in data:
            f.write(f"{d.get('ip')}:{d.get('port')}")
            if d.get("domain"):
                f.write(f" {d.get('domain')}:{d.get('port')}")
            else:
                f.write(" None")
            f.write(f" {d.get('time')}\n")


def out_to_json(data, file_name):
    values = []
    for d in data:
        values.append({
            "ip": d.get("ip"),
            "port": d.get("port"),
            "domain": d.get("domain"),
            "time": d.get("time")
        })

    with open(file_name, "w") as f:
        json.dump(values, f, indent=4)


def main(args):
    resp_data = None
    if args.query:
        resp_data = quake_query(args.query)

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
            out_to_txt(resp_data, args.file if args.file else f"{out_name_prefix}.txt")
        elif args.output == "json":
            # output to json
            out_to_json(resp_data, args.file if args.file else f"{out_name_prefix}.json")
        elif args.output == "all":
            # output to both
            out_to_txt(resp_data, args.file if args.file else f"{out_name_prefix}.txt")
            out_to_json(resp_data, args.file if args.file else f"{out_name_prefix}.json")
        else:
            print("Invalid output format")


if __name__ == "__main__":
    args = args.parse_args()
    main(args)

