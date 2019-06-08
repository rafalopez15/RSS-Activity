#Given a Dictionary keyed by Company and valued by RSS feed url,
#write a function that determines which companies had no activity
#for a given number of days.
from datetime import datetime
import requests
import os
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
        A date in string format
    """
    for child in root:
        if child.tag == 'channel':
            for channel in child:
                if channel.tag == 'item':
                    for item in channel:
                        if item.tag == 'pubDate':
                            return item.text

def get_inactivity(days):
    tree = ET.parse('rss_feed.xml')
    root = tree.getroot()
    date = find_date(root)[5:25]
    date_obj = datetime.strptime(date, '%d %b %Y %H:%M:%S')
    current_date = datetime.now()
    return abs((current_date - date_obj).days) >= days

def find_inactivity_for_days(days):
    for company, rss_feeds in data.items():
        if isinstance(rss_feeds, list):
            for feed in rss_feeds:
                get_xml(feed)
                if get_inactivity(days):
                    print('{} had no activity for {} days'.format(company, days))
        else:
            get_xml(rss_feeds)
            if get_inactivity(days):
                print('{} had no activity for {} days'.format(company, days))

    #os.remove('rss_feed.xml')

find_inactivity_for_days(1)
