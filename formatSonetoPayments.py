#!/usr/bin/env python3

import sys
import pandas as pd

def formatPaymentsExport(dfile):
    dfile.drop("textbox2","textbox48","textbox20","textbox50","textbox13","textbox18","textbox17","textbox8","textbox22","textbox15")

    # Add new header
    dfile.columns = ['Client','PostingDate','AmountPaid','PaymentNo','Invoice','ServiceDate','Service')

    # Remove first row (unneeded text)
    dfile.drop(['0'], axis='0')

    # Format dates
    dfile = pd.to_datetime(df.PostingDate)
    dfile = pd.to_datetime(df.ServiceDate)
    dfile['PostingDate'] = dfile['PostingDate'].dfile.strftime('%m/%d/%Y')
    dfile['ServiceDate'] = dfile['ServiceDate'].dfile.strftime('%m/%d/%Y')

    # Change payment values to positive
    dfile.loc['AmountPaid'] *= -1

    return dfile

dfile = pd.read_tocsv(sys.argv[1])
df = formatPaymentsExports(dfile)
return df
