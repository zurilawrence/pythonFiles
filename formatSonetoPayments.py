#!/usr/bin/env python3

#  Created by Zuri Lawrence on 12/31/19.
#  Copyright © 2019 Zuri Lawrence. All rights reserved.

import sys
import pandas as pd

def formatPayments(dfile):
    dfile.rename(columns={"textbox31":"Client","textbox57":"PostingDate","textbox6":"AmountPaid","textbox7":"PaymentNo","textbox32":"Invoice",
    "textbox43":"ServiceDate"},inplace=True)

    # Format dates
    dfile['PostingDate'] = pd.to_datetime(dfile.PostingDate)
    dfile['ServiceDate'] = pd.to_datetime(dfile.ServiceDate)
    dfile['PostingDate'] = dfile['PostingDate'].dt.strftime('%m/%d/%Y')
    dfile['ServiceDate'] = dfile['ServiceDate'].dt.strftime('%m/%d/%Y')

    # Change payment values to positive
    for idx in range(len(dfile.index)):
        dfile.loc[idx, 'AmountPaid'] = float(dfile.loc[idx, 'AmountPaid'])

    return dfile

dfile = pd.read_csv(sys.argv[1])
formatPayments(dfile)
