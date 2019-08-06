import email, getpass, imaplib, os, datetime, getpass, sys, smtplib, time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


user = 'jrbruten1@sheffield.ac.uk'   # address to download and send email from
pwd = getpass.getpass("Enter Password: ")   # password for above email - entered when running script
recipient = 'jrbruten1@sheffield.ac.uk'    # recipient email address - no password needed, can be above email 


def keyword(article, list1, list2):
   # search through the lists of keywords. If want to keep abstract return True, else False
    article = article.lower()
    if 'astro2020' in article:
        return False
    n2 = 0
    for item in list1:              
        item = item[:-1]
        if article.find(item) >= 0:
            return True                 # for list 1 keep abstract if only 1 word present
    for item in list2:
        item = item[:-1]
        if article.find(item) >= 0:
            n2+=1
        if n2==2:
            return True                 # for list 2 require 2 words to keep abstract
    return False    

# load in keywords from files
keywords1 = []
keywords2 = []
k1 = open("keywords1.txt", "r")
k2 = open("keywords2.txt", "r")
for line in k1:
    keywords1.append(line)
for line in k2:
    keywords2.append(line)
k1.close()
k2.close()

# create today string - todays date in format for SENTON below
now = datetime.datetime.now()
month_list = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
month = now.month
month = month_list[month-1]
day = now.day
year = now.year
today = str(day)+'-'+str(month)+'-'+str(year) # this is required format for the date

no_message = False

# search inbox for email from arxiv sent today
# open relevant mailbox
mail = imaplib.IMAP4_SSL("imap.gmail.com") # connect to host using ssl
mail.login(user,pwd)
mail.select("Inbox")   # choose mailbox to search in
# search through mailbox for specific email - None means no CHARSET
typ, item = mail.search(None, 'FROM', 'no-reply@arxiv.org', 'SENTON', today)
# returns a list of emails
items = item[0].split()
if len(items)==0:
    no_message = True

if no_message==False:
    # print out arxiv email to a temporary file to read through
    tempfile = open("arxiv_temp.txt", "w")
    for emailid in items:
        typ, data = mail.fetch(emailid, '(RFC822)')  # gets the data from the email - RFC822 idicates ASCII
        email_body = data[0][1]
        msg = email.message_from_bytes(email_body)
        tempfile.write(msg.get_payload())   # this writes out the main body text of the email 

    outfile = open("arxiv.txt", "w")     # final file to write chosen abstracts to
    outfile.write("arXiv abstracts ")
    outfile.write(today)
    outfile.write("\n\n")
    av = open("arxiv_temp.txt", "r")     # temp arxiv file to read from
    article = str()                # empty string to write each article to 
    count = 0
    start_record = False         
    for line in av:               # step through each email
        if line[0:20] == '%-%-%-%-%-%-%-%-%-%-':   # stop reading once reach cross-listings
            abs_flag = keyword(article, keywords1, keywords2)
            if abs_flag == True:
                outfile.write(article)
                count+=1
            break
        article_stop = False        
        if start_record == False:      # only start reading once reached the first abstract
            if line[0:6] == 'arXiv:':
                start_record = True
        if start_record == True:        # if first abstract has been reached     
            if line[0:10] == '----------':   # this marks the end of the abstract
                article_stop = True
                article = article + line     # append article string with current line
            if article_stop == False:
                article = article + line     # append article string with current line
            if article_stop == True:         # once end of article reached
                abs_flag = keyword(article, keywords1, keywords2)
                if abs_flag == True:
                    outfile.write(article)   # write abstract to outfile 
                    count+=1    
                article = str()     # reset article string to be empty for the next article

    outfile.write("\nTotal Abstracts Today: ")
    outfile.write(str(count))

    av.close()    # close open files
    outfile.close()
    os.remove("arxiv_temp.txt")    # remove the temporary file

    tempfile.close()   # close temporary file

mail.close()    # close email connection
mail.logout()

server = smtplib.SMTP('smtp.gmail.com', 587)
server.ehlo()
server.starttls()
server.ehlo()
server.login(user, pwd)    # login again in order to send mail

msg = MIMEMultipart()

if no_message==False:    # create message to send
    msg_str = str()
    msg_file = open("arxiv.txt", "r")
    for line in msg_file:
        msg_str = msg_str + line
    msg['Subject'] = 'arXiv Abstracts ' + today + ' --- ' + str(count) + ' total'
    os.remove("arxiv.txt")
else:
    msg_str = 'No arxiv email on ' + today
    msg['Subject'] = msg_str

msg['From'] = user
msg['To'] = recipient
msg.attach(MIMEText(msg_str, 'plain'))
text = msg.as_string()
server.sendmail(user, recipient, text)
server.close()