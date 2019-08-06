import yagmail


user = 'astro.coffee.sheffield@gmail.com'   # address to download and send email from
pwd = 'crack_astro'
recipient = []

contents = '🔭☕ Astro Coffee at 10:00 in the Austin Room ☕🔭 \n\n Sent by CRACKbot'

with open('emails.txt') as f:
    recipient.extend(f.read().split())
yag = yagmail.SMTP(user, pwd)
yag.send(recipient, "🔭☕ Astro COFFEE at 10:00 ☕🔭", contents) 