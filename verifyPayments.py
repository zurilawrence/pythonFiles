#  Created by Zuri Lawrence on 12/31/19.
#  Copyright © 2019 Zuri Lawrence. All rights reserved.

import pandas as pd
import sys
import formatSonetoPayments as FSP
from flask import Flask
from flask_mail import Mail
from flask_mail import Message

def emailResults():
    mail = Mail()
    app = Flask(__name__)
    mail.init_app(app)

    f = open("resultMessage.txt", "r")
    message = f.read()
    f.write(datetime.today().date + ".")
    f.close()

    with open("recipients.txt") as f:
        msg = Message(recipients=f.readline(),
                sender=f.readline(),
                body=message,
                subject="Billing reconciliation")

    # Attach csv of errors
    with app.open_resource("billingAlerts.csv") as fp:
        msg.attach("billingAlerts.csv","billingAlerts/csv",fp.read())

    # Send mail
    mail.msg(msg)

def selectMissedPayments(rep):
    # Missing payments in report record are sent to be emailed
    pass

def authorizePayments(pay,rep):
    # For every row in report SELECT column from payment record
    for idx in range(len(pay.index)):

        client = rep.loc[idx, 'Client']
        startDate = rep.loc[idx, 'Start Date']
        serviceCode = rep.loc[idx, 'Service']

        # Date Billed
        rep.loc[idx, 'DateBilled'] = rep.loc[pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode)].index, 'PostingDate']
        # Amount Paid
        rep.loc[idx, '$ Paid'] = pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode), ['AmountPaid']]
        # Check Number
        rep.loc[idx, 'DateBilled'] = pay[(pay['Client']==client) & (pay['ServiceDate']==startDate) & (pay['ServiceCodeName']==serviceCode), ['PaymentNo']]



formattedFile = FSP.formatPayments(pd.read_csv(sys.argv[1]))
reportToSend = pd.read_csv(sys.argv[2])

authorizePayments(formattedFile,reportToSend)
