# RSS-Activity

## Using **Python 3** this program determines if a Company which uses RSS feeds has had no activity for a given number of days.

### Using and XML parser the program finds the last updated title posted and then converts it into a date format to find the difference and detemine if that difference is greater or equal to the days give to check for no activity.

### To run this program:
```
python3 InactivityForDays.py
```
### You can change the source code to pass in a different number of days.

### Potential bugs that may arise.
- Some RSS feeds XML files do not contain the same tag for finding the last update. This is an issue
because this program only finds for the tag "pubDate" in the XML tree structure.