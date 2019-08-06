import email, getpass, imaplib, os, datetime, getpass, sys, smtplib, time

# create today string - todays date in format for SENTON below
now = datetime.datetime.now()
month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
month = now.month
month = month_list[month-1]
day = now.day
year = now.year
today = str(day)+'-'+str(month)+'-'+str(year) # this is required format for the date

# create list of emails
email_list = []
f = open("emails.txt")
for line in f:
    email_list.append(line[:-1])

f.close()

user = 'astro.coffee.sheffield@gmail.com'   # address to download and send email from
pwd = 'crack_astro'

mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(user,pwd)
mail.select("Inbox")
typ, item = mail.search(None, 'SENTON', today)
items = item[0].split()

del_inds = []

for emailid in items:
    typ, data = mail.fetch(emailid, '(RFC822)')  # gets the data from the email - RFC822 idicates ASCII
    email_body = data[0][1]
    msg = email.message_from_bytes(email_body)
    sender = email.utils.parseaddr(msg['From'])
    subject = msg['Subject']
    if subject != 'unsubscribe' and subject != 'subscribe':
        continue
    sender = sender[-1]
    if subject == 'unsubscribe':
        for i in range(0, len(email_list)):
            if email_list[i]==sender:
                del_inds.append(i)
    else:
        if sender not in email_list:
            email_list.append(sender)

mail.close()    # close email connection
mail.logout()
    
for val in del_inds:
    email_list.pop(val)

f = open('emails.txt', 'w')
for item in email_list:
    f.write(item)
    f.write('\n')
f.close()

