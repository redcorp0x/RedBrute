#!/usr/bin/env python3

from urllib.parse import urlparse
import argparse
import config
import banner
import sys
import engine


parser = argparse.ArgumentParser(usage=argparse.SUPPRESS)
parser.add_argument("-u", "--url", required=True, help="Specify the target URL")
parser.add_argument("-m", "--fail-message", help="Specify the error message returned for failed requests", required=True)
parser.add_argument("--wordlist", help="Specify a custom wordlist)", required=True)

# Optional Arguments
parser.add_argument("--data", help="Specify the HTTP request data", default=None)
parser.add_argument("--param", help="Specify the parameter to be tested", default=None)
parser.add_argument("--auth-param", help="Specify the valid parameter for http-get request", default=None)
parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
parser.add_argument("-k", "--verify", action="store_true", help="Disable SSL certificate verification")
parser.add_argument("--cookie", help="Specify HTTP cookies", default=None)
parser.add_argument("--header", help="Specify custom HTTP headers", default=None)
parser.add_argument("--proxy", help="Specify a proxy URL for request debugging and interception", default=None)
parser.add_argument("--timeout", help="Specify the request timeout in seconds. Defaults to 4 seconds", default=4, type=int)
parser.add_argument("--batch-size", help="Specify the number of words loaded per batch (default: 1000)", default=1000, type=int)
parser.add_argument("--thread-counts", help="Specify the number of concurrent worker threads (default: 100)", default=100, type=int)
parser.add_argument("--method", help="HTTP input method: gu (GET URL), gf (GET Form), pf (POST Form)", default="pf",choices=["gu", "gf", "pf", "get-url", "get-form", "post_form"])
methods = {
    "gu":"get_url",
    "get-url":"get-url",
    "gf":"get-form",
    "get-form":"get-form",
    "pf":"post-form",
    "post-form":"post-form"
}
args = parser.parse_args()
method = methods[args.method]
parse_url = urlparse(args.url)

if parse_url.scheme not in ("http", "https") or not parse_url.netloc:
    print("Invalid URL provided")  
    sys.exit(1)     
if args.proxy is not None:
    parse_proxy = urlparse(args.proxy)
    if parse_proxy.scheme not in ("http", "https") or not parse_proxy.netloc:
        print("Invalid URL provided")
        sys.exit(1)
        
print("[!] Initializing Configurations...")
config.url = args.url
config.wordlist = args.wordlist
config.verbose = args.verbose
config.verify = args.verify
config.failure_message = args.fail_message
config.header = args.header
config.cookie = args.cookie
config.data = args.data
config.vulnerable = args.param
config.proxy = args.proxy
config.method = method
config.timeout = args.timeout
config.batch = args.batch_size
config.thread = args.thread_counts
config.auth = args.auth_param
print("[!] Configuration Initialized.\n")

#Calling the main check function
engine.threader()
