    # hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    newdates = []
    for date in old_dates:
        reformatted_dates = datetime.strptime(date, '%Y-%m-%d').strftime('%d %b %Y')
        newdates.append(reformatted_dates)
    return newdates


def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if isinstance(start, str) is False:
        raise TypeError(" start must be a string")
    if isinstance(n, int) is False:
        raise TypeError(" n must be a int")

    r_date = datetime.strptime(start, '%Y-%m-%d')
    res = [r_date]
    for i in range(n-1):
        r_date += timedelta(days=1)
        res.append(r_date)
    return res

def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    date_list = date_range(start_date, len(values))
    res = list(zip(date_list, values))
    return res


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    charge = defaultdict(float)
    with open(infile, 'r') as file:
        reader = DictReader(file)
        for r in reader:
            days = (datetime.strptime(r['date_returned'], '%m/%d/%Y') - datetime.strptime(r['date_due'], '%m/%d/%Y')).days
            if days<0:
                latefee = 0.00
            else:
                latefee = days*0.25
                charge[row['patron_id']] += latefee

    with open(outfile, 'w', newline = '') as file:
        fieldnames = ['patron_id', 'late_fees']
        outfile = DictWriter(file, fieldnames = fieldnames)
        outfile.writeheader()
        for patron_id, latefee in charge.items():
            outfile.writerows({'patron_id' : patron_id, 'late_fees' : f"{latefee:.2f}"})
    

# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
