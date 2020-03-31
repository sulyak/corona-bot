import requests
from lxml import html

URL = "https://www.worldometers.info/coronavirus/"
COUNTER_XPATH = "//*[@id='maincounter-wrap']/div/span/text()"

class CoronaCounter:
    def __init__(self, tuple_data):
        self.cases = tuple_data[0]
        self.deaths = tuple_data[1]
        self.recovered = tuple_data[2]
        self.all_data = tuple(tuple_data)

def counter_from_country(country: str=None):
    """Get the counter from specific country.
    `param country`: the specif country as str\n
    `Return Value`: A Counter object

    If no param were given, the worldwide counter will be returned.\n
    An exception will be raise if the given country does not exist
    """

    # check if country was given as argument
    if country:
        country_url = URL + "/country/" + country
    else:
        country_url = URL

    # load the page tree
    page = requests.get(country_url)
    html_tree = html.fromstring(page.content)

    # assert that country exist
    if html_tree.find(".//title").text == "404 Not Found":
        raise NameError("Country \'%s\' not recorded" % country)

    data = html_tree.xpath(COUNTER_XPATH)
    return CoronaCounter(data)

def does_country_exist(country: str):
    country_url = URL + "/country/" + country
    page = requests.get(country_url)
    html_tree = html.fromstring(page.content)
    return html_tree.find(".//title").text != "404 Not Found"

def main():
    import sys
    print(counter_from_country(sys.argv[1]).cases)

if __name__ == "__main__": main()
