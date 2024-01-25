# recon-py

A tool which call quake API

## Config

Before running the script, a file named `quake.conf` need to be created.
The file should contain the following information:

```text
X-QuakeToken: <your-quake-token>
size: <number-of-results>
<header-key>: <header-value>
```

Any other data you want to add to header can follow the same format

## Usage

```bash
usage: quake.py [-h] [-q QUERY] [-o {txt,json,all}] [-st START_TIME] [-et END_TIME]

Quake API in python

options:
  -h, --help            show this help message and exit
  -q QUERY, --query QUERY
                        Query to search
  -o {txt,json,all}, --output {txt,json,all}
                        Output format
  -st START_TIME, --start-time START_TIME
                        Start time of the query, format YYYY-mm-dd HH:MM:SS UTC
  -et END_TIME, --end-time END_TIME
                        End time of the query, format YYYY-mm-dd HH:MM:SS UTC
```

By default, the output filename will be `<query>.{txt,json}` where `: `, `:`, ` ` will be replaced by `_`.

## Example

```bash
python quake.py -q "domain: example.com AND service: http" -o all
```

Two output file will be:

- `domain_example.com_AND_service_http.txt`
- `domain_example.com_AND_service_http.json`
