#Given a Dictionary keyed by Company and valued by RSS feed url,
#write a function that determines which companies had no activity
#for a given number of days.
from datetime import datetime
import requests
import math
import xml.etree.ElementTree as ET

# Sample data used to test code
data = {
    'BBC': ['http://feeds.bbci.co.uk/news/world/rss.xml', 'http://feeds.bbci.co.uk/news/world/rss.xml'],
    'Real Time with Bill Maher': 'http://billmaher.hbo.libsynpro.com/rss',
    'Bill Simmons Podcast': 'https://rss.art19.com/the-bill-simmons-podcast'
}

# Function to get RSS Feed in XML via HTTP request.
def get_xml(url):
    """
    Writes an XML file pulled from a company file to the local directory.

    Parameters
    ----------
    url : str
        Takes in a url as a string that should contain the RSS Feed URL.
    """
    response = requests.get(url)
    with open('rss_feed.xml', 'wb') as file:
        file.write(response.content)

# Function to find the date in which the last update was published
def find_date(root):
    """
    Takes the root of the XML tree and finds a tag which contains the date of the last updated item.

    Parameters
    ----------
    root : Element
        A root to the elements of the tree.
    
    Returns
    -------
    str
        A date in string format.
    """

    # Search XML tree for first 'pubDate' tag which corresponds to the latest publish date
    tree = ET.parse('rss_feed.xml')
    root = tree.getroot()
    try:
        return next(root.iter('pubDate')).text # The iterable object is the list of matches found
    except StopIteration:
        return '' # Return empty string if no element matches were found

def get_inactivity(days):
    """
    Parses XML from RSS feed and returns the difference in days from the last update.

    Parameters
    ----------
    days : int
        Number of to days to check if there was any activity.
    
    Returns
    -------
    bool
        Compares the difference from last update with current date and returns True or False
        if the difference is larger that 'days' given.
    """
    tree = ET.parse('rss_feed.xml')
    root = tree.getroot()
    # Uses find_date function to get date from RSS feed and converts string into datetime object
    last_update = datetime.strptime(find_date(root)[5:25], '%d %b %Y %H:%M:%S')
    current_date = datetime.now()
    # Calculates the difference in days and compares against the parameter days
    return math.floor((current_date - last_update).days) >= days

def find_inactivity_for_days(days):
    """
    Given a dictionary of Companies and RSS feeds, determines which company has had no activity
    for a given number of days.

    Prints those companies which have had no activity for the given number of days.

    Parameters
    days : int
        Number of day to check for no activity.
    """
    for company, rss_feeds in data.items():
        # It is possible that a company contains multiple RSS feeds
        # this condition checks to see if that is the case and iterates through
        # that company's RSS feeds.
        if isinstance(rss_feeds, list):
            for feed in rss_feeds:
                get_xml(feed)
                if get_inactivity(days):
                    print('{} had no activity for {} days'.format(company, days))
        else:
            get_xml(rss_feeds)
            if get_inactivity(days):
                print('{} had no activity for {} days'.format(company, days))


find_inactivity_for_days(1)
