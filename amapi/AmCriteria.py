################################################################################
# requires non-standard python packages:
#   `pip install pytz`
################################################################################
import pytz
from datetime import datetime, timedelta

class AmCriteria:

    def __init__(self, beg_date=None, end_date=datetime.today(), t_minus_days=None, app=None, vendor=None, verbosity=0):
        self.end_date = end_date.replace(tzinfo=pytz.UTC)
        if beg_date is not None:
            self.beg_date = beg_date.replace(tzinfo=pytz.UTC)
        elif t_minus_days is not None:
            self.beg_date = self.end_date - timedelta(days=t_minus_days)
        self.app = app
        self.vendor = vendor
        self.t_minus_days = t_minus_days
        self.verbosity = verbosity
