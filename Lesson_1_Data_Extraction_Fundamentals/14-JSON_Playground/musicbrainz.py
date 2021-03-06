# Initial code provided by Udacity as part of Nanodegree study program.  Forked from https://github.com/udacity/ud032 Altered by jamey mcCabe and run locally.
import json
import requests


BASE_URL = "http://musicbrainz.org/ws/2/"
ARTIST_URL = BASE_URL + "artist/"

query_type = {  "simple": {},
                "atr": {"inc": "aliases+tags+ratings"},
                "aliases": {"inc": "aliases"},
                "releases": {"inc": "releases"}}


def query_site(url, params, uid="", fmt="json"):
    params["fmt"] = fmt
    r = requests.get(url + uid, params=params)
    print "requesting", r.url

    if r.status_code == requests.codes.ok:
        return r.json()
    else:
        r.raise_for_status()


def query_by_name(url, params, name):
    params["query"] = "artist:" + name
    return query_site(url, params)


def pretty_print(data, indent=4):
    if type(data) == dict:
        print json.dumps(data, indent=indent, sort_keys=True)
    else:
        print data


def main():
    # Section Prompts for Artist to search on and gives list of them so you can select 1
    artist = raw_input("What artist should we search for? ")
    results = query_by_name(ARTIST_URL, query_type["simple"], artist)
    print "Found %d artists:" % len(results["artists"])
    for xref in range (0,len(results["artists"])-1):
        if "disambiguation" in results["artists"][xref]: print "xref:%d - name:%s - Disambig:%s" % (xref, results["artists"][xref]["name"], results["artists"][xref]["disambiguation"])
        else: print  "xref: %d - name:%s - Disambig: %s" % (xref,results["artists"][xref]["name"], "no disambiguation found")
    artistXref = int(float(raw_input("Which of those artists should we use? or type 99 to list all artists and their begin-area(s) ")))


    #section searches for any tags begin-area
    if artistXref == 99:
        for xref in range (0,len(results["artists"])-1):
            artistData = results["artists"][xref]
            if "begin-area" in artistData: 
                print "xref: %d name: %s begin-area:" % (xref,results["artists"][xref]["name"])
                pretty_print (artistData["begin-area"])
            else: print  "xref: %d name: %s %s" % (xref, results["artists"][xref]["name"],"no begin-area found")
    else:

        #section gives more info on one artist 
        artist_id = results["artists"][artistXref]["id"]
        print "\nARTIST:"
        pretty_print(results["artists"][artistXref])

        artist_data = query_site(ARTIST_URL, query_type["releases"], artist_id)
        releases = artist_data["releases"]
        print "\nONE RELEASE:"
        pretty_print(releases[0], indent=2)
        release_titles = [r["title"] for r in releases]

        print "\nALL TITLES:"
        for t in release_titles:
            print t


if __name__ == '__main__':
    main()
