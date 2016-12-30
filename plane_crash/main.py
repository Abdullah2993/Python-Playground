"""
Plane crash dbs
"""
import urllib2
from argparse import ArgumentParser
from csv import writer, QUOTE_ALL
from bs4 import BeautifulSoup


def get_page(page_no):
    """get page source"""
    source = ""
    try:
        req = urllib2.Request(r"http://www.planecrashinfo.com/{0}/{0}.htm".format(page_no))
        source = urllib2.urlopen(req).read()
    except urllib2.URLError:
        pass
    finally:
        pass
    return source

if __name__ == '__main__':
    PARSER = ArgumentParser("Download plane crash DB as CSV")
    PARSER.add_argument("start", help="Starting year", type=int)
    PARSER.add_argument("end", help="End Year", type=int)
    PARSER.add_argument("output", help="Output file")
    ARGS = PARSER.parse_args()

    START = ARGS.start
    END = ARGS.end + 1

    with open(ARGS.output, 'wb') as csvfile:
        WRITER = writer(csvfile, quoting=QUOTE_ALL)
        HEADERS = ["Date", "Location", "Operator", "Aircraft Type", "Registration", "Fatalities"]
        WRITER.writerow(HEADERS)
        for i in range(START, END):
            page = get_page(START)
            soup = BeautifulSoup(page, 'html.parser')
            table = soup.find("table")
            for row in table.find_all("tr")[1:]:
                tag = [col.font for col in row.find_all("td")]
                strings = [list(t.stripped_strings) for t in tag]
                flat = [x.encode("utf-8") for l in strings for x in l]
                WRITER.writerow(flat)
