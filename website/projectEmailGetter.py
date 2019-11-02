import imaplib
import re
def getEmailsIMAP(server,user,password,ssl=False,port=None,start=0,count=5):
    if not port:
        port = 993 if ssl else 143
    imap = imaplib.IMAP4_SSL(server, port) if ssl else imaplib.IMAP4(server, port)
    auth=imap.login(user, password)[0]
    if "OK" in auth:
        imap.select('Inbox')
        emails=imap.search(None,'ALL')[1][0].split()
        length=len(emails)-1
        returnArray=[]
        for i in range(length-start-count,length-start):
            returnArray.append(imap.fetch(emails[i+1],'(RFC822)')[1][0][1])
        imap.close()
        return returnArray
    else:
        imap.close()
        raise Exception
def getBriefFromEmails(emails):
    briefs=[]
    for email in emails:
        utfemail=email.decode("utf-8")
        subject=""
        sender=""
        date=""
        #print(utfemail)
        for line in utfemail.split("\n"):
            if subject=="" and re.match('Subject:',line):
                subject=line
            elif sender=="" and (re.match('Sender:',line) or re.match('From:',line)):
                sender=line
            elif date=="" and re.match('Date:',line):
                date=line
        briefs.append((sender,date,subject))
    return briefs
def getContentFromEmails(emails):
    contents=[]
    for email in emails:
        utfemail=email.decode("utf-8")
        boundary=""
        capture=0
        content=""
        for line in utfemail.split("\n"):
            if boundary=="":
                match=re.match(r'.*boundary\=\"(.*)\"',line)
                if match:
                    boundary=match.group(1);
            else:
                if boundary in line:
                    capture+=1
                elif capture==2:
                    if content!="":
                        content+="\n"
                    content+=line
           # elif sender=="" and (re.match('Sender:',line) or re.match('From:',line)):
            #    sender=line
            #elif date=="" and re.match('Date:',line):
             #   date=line
        contents.append(content)
    return contents
#print(getContentFromEmails(getEmailsIMAP("imap.gmail.com","mdr.brook@gmail.com","mmjixwvaxdwndlfc",ssl=True)))
