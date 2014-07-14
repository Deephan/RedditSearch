# RedditSearch
# Author: Deephan Mohan
# Version 1.0
# Last modified: July 14, 2014

# This program is "public domain": you may copy, modify, run,
# publish, distribute, embed, and/or use this program in any way 
# whatsoever without prior permission and/or giving me any 
# credit or payment whatsoever.
# (Indeed, please don't bother me to ask such permission!)
# It comes "as is" with no warranties or guarantees of any kind.
# It may contain bugs and/or be inconsistent with its internal
# or usage documentation.  
# Have fun with it!
# (Of course, this really needs a nice GUI, rather than this
# console interface!)


usage_string = """\

RedditSearch - starts the search in console mode and prints the response to console or a dump file. 
			   Results of the feed are sorted by author 

Usage: RedditSearch.py <source_options> <values> 

	(i.e) RedditSearch -q <queryTerm> -f <format> (optional) -o <output file> (optional)

	<source_options> specifies one or more switches for defining the search
		-q   defines the query term to be searched
		-f   defines the type of the final output (optional)
		-o   defines the name of the dump file (optional)

	-q   can take any string

	-f   can be json, yaml or xml 
		-   if source option or value is not provided it defaults to json

	-o  can be any string 
		-   if source option is not provided, the output is printing on the console
		-   if value is not provided it creates the dump file in the name of the query term with appropriate type

Examples: 

	RedditSearch -q subreddit:fifa                      # Performs a reddit search and prints the JSON response to console
	RedditSearch -q subreddit:fifa	-f  json            # Performs a reddit search and prints the JSON response to console
	RedditSearch -q subreddit:fifa	-f  xml             # Performs a reddit search and prints the XML response to console
	RedditSearch -q subreddit:fifa	-f  yaml            # Performs a reddit search and prints the YAML response to console
	RedditSearch -q subreddit:fifa	-f  json  -o        # Performs a reddit search and dumps the JSON response to subreddit:fifa.json
	RedditSearch -q subreddit:fifa	-f  xml   -o        # Performs a reddit search and dumps the XML response to subreddit:fifa.xml
	RedditSearch -q subreddit:fifa	-f  yaml  -o        # Performs a reddit search and dumps the YAML response to subreddit:fifa.yaml
	RedditSearch -q subreddit:fifa	-f  json  -o  foo   # Performs a reddit search and prints the JSON response to foo.json


"""

import urllib
import urllib2
from urllib2 import HTTPError, URLError
import json
import sys
import yaml
import HTMLParser

resp = ""

def getRedditResponse(query, type):
    global resp
    if type == ".yaml": type = ".json" # YAML format can be gotten from the same JSON serializer
    Url = "http://www.reddit.com/search"+type+"?q=" + query
    try:
        resp = urllib2.urlopen(Url) # To get header information add urlopen().info()
    except HTTPError:
        print('The server couldn\'t fulfill the request.')
    except URLError:
        print('We failed to reach a server.')
    return

def create_file(file, format, dumpOutputToFile):
    global resp
    output = ""
    h = HTMLParser.HTMLParser()
    if format == "json": 
        raw_output = json.dumps(json.load(resp)) # Processing JSON response
        output = json.loads(raw_output)
        output["data"]["children"] = sorted(output["data"]["children"], key = lambda l: l["data"]["author"].lower())
        output = h.unescape(json.dumps(output, indent=4))
    elif format == "xml": 
    	output = h.unescape(resp.read())
    elif format == "yaml": 
        raw_output = json.dumps(json.load(resp)) # (parse json response into yaml) 
        output = json.loads(raw_output)
        output["data"]["children"] = sorted(output["data"]["children"], key = lambda l: l["data"]["author"].lower())
        output = h.unescape(yaml.dump(output))
    if dumpOutputToFile == True:
		try:
			f = open(file, "w+")
		except IOError as e:
			print("I/O error({0}): {1}".format(e.errno, e.strerror))
		else:
			f.write(output) 
			f.close()       
    else:
        print(output)
    return


def main():
    global resp
    queryTerm = output_format = outfile = ""
    set_query_term = set_format = set_output = False
    if len(sys.argv)==1 or "-q" not in sys.argv:
        print(usage_string)
        return
    output_format = ".json"
    for arg in sys.argv[1:]:
        if set_query_term == True:
            queryTerm = arg
            set_query_term = False
        if set_format == True:
            if arg.lower() == "json": output_format = ".json"
            elif arg.lower() == "xml": output_format = ".xml"
            elif arg.lower() == "yaml": output_format = ".yaml"
            set_format = False
        if set_output == True: outfile = arg+output_format
        if arg[:2] == "-q": set_query_term = True
        elif arg[:2] == "-f": set_format = True
        elif arg[:2] == "-o": set_output = True
    # make request
    getRedditResponse(queryTerm, output_format)
    # If no output file is specified create it from the name of the query term and output format
    if outfile == "": outfile = queryTerm+output_format
    if output_format == ".json": create_file(outfile, "json", set_output)
    elif output_format == ".xml": create_file(outfile, "xml", set_output) 
    elif output_format == ".yaml": create_file(outfile, "yaml", set_output)
    
    
main()
