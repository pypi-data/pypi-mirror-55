# ELB Log Tools

Tools for processing logs from AWS Elastic Load Balancer

## Installation

```
$ pip install elb-log-tools
```

## Usage

### Specifying the log bucket name

There are two options:

1. Set the ``ELB_LOG_BUCKET`` environment variable, or
2. Pass the bucket name to ``elb-logs`` using the ``-b`` or ``--bucket`` argument.

   ```
   $ elb-logs -b my-log-bucket
   ```

### Print ELB logs to stdout
```
$ elb-logs | head -n 1
2019-11-06T23:00:47.799875Z production-pymcore-webserver 84.10.79.236:55801 172.16.11.238:80 0.000049 1.922708 0.000054 200 200 0 230454 "GET https://www.pymetrics.com:443/results/downloads/traits/ HTTP/1.1" "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2
```

### Filter ELB logs

Filtering currently only outputs the PATH component of the log file.

```
# Only output redirects
$ elb-logs | elb-filter --include-statuses 301 302 | head -n 1
/logout/
```

### Aggregate request counts based on pattern matching

``elb-patterncounts`` matches URL paths against a list of regex patterns, and
outputs the counts of requests matching the patterns in CSV format.

```
# patterns.txt has all the URL patterns we want included in the report

$ elb-logs | elb-filter -f 404 | elb-patterncounts --patternfile patterns.txt --all
Path,Hits
/api3/apps/applications/,66762
/api3/games/games/,42192
/api/game/submission/,35418
/api2/games/list/,33487
/api2/accounts/config/,19251
/health/,18891
```

## Examples

### Get most common requests for static files that 404:

```
$ elb-logs | elb-filter -i 404 | grep static | head -n 50 | uniq -c | sort -bgr
```
