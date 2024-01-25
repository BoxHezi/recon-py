# recon-py


A tool which call quake API

## Config

Prior to use the script, a file named `quake.conf` need to be created.
The file should contain the following information:

```text
X-QuakeToken: <your-quake-token>
size: <number-of-results>
<header-key>: <header-value>
```

Any other data you want to add to header can follow the same format

## Usage

```bash
usage: quake.py [-h] [--query QUERY] [--output {txt,json,all}] [--file FILE]

Quake API in python

options:
  -h, --help            show this help message and exit
  --query QUERY, -q QUERY
                        Query to search
  --output {txt,json,all}, -o {txt,json,all}
                        Output format
  --file FILE, -f FILE  File to save the output
```

By default, the output filename will be `<query>.{txt,json}` where `: `, `:`, ` ` will be replaced by `_`

## Example

```bash
python quake.py -q "domain: example.com AND service: http" -o all
```

Two output file will be:
- `domain_example_com_service_http.txt`
- `domain_example_com_service_http.json`
