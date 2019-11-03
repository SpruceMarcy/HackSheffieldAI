import imaplib
import re
import base64
import quopri
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
#def getHTMLFromEmails(emails):
#    contents=[]
#    for email in emails:
#        utfemail=email.decode("utf-8")
#        boundary=""
#        capture=0
#        content=""
#       for line in utfemail.split("\n"):
#            if boundary=="":
#                match=re.match(r'.*boundary\=\"(.*)\"',line)
#                if match:
#                    boundary=match.group(1);
#            else:
#                if boundary in line:
#                    capture+=1
#                elif capture==2:
##                    if content!="":
#                        content+="\n"
#                    content+=line
#           # elif sender=="" and (re.match('Sender:',line) or re.match('From:',line)):
#            #    sender=line
#            #elif date=="" and re.match('Date:',line):
#             #   date=line
#        contents.append(content)
#    return contents
def getPlainFromEmails(emails):
    contents=[]
    for email in emails:
        utfemail=email.decode("utf-8")
        boundary=""
        capture=0
        transEnc=""
        content=""
        for line in utfemail.split("\n"):
            if boundary=="":
                match=re.match(r'.*boundary\=\"(.*)\"',line)
                if match:
                    boundary=match.group(1);
            else:
                if boundary in line:
                    capture+=1
                elif capture==1 or capture==2:
                    capture+=1
                    match=re.match(r'.*Content-Transfer-Encoding:(.*)',line)
                    if match:
                        transEnc=match.group(1).strip()
                elif capture==3:
                    if transEnc=="base64":
                        content+= base64.decodebytes(line.encode()).decode("utf-8")
                    elif transEnc=="quoted-printable":
                        content+=quopri.decodestring(line.encode()).decode("ISO-8859-1")
                    else:
                        if content!="":
                            content+="\n"
                        content+=line
        if content=="":#FALLBACK
            match=re.search(r'Content-Transfer-Encoding: +(base64|quoted-printable|utf-7)',utfemail)
            if match:
                transEnc=match.group(1).strip()
            if transEnc=="base64":
                utfemail= base64.decodebytes(utfemail.encode()).decode("utf-8")
            elif transEnc=="quoted-printable":
                utfemail=quopri.decodestring(utfemail.encode()).decode("ISO-8859-1")
            utfemail=re.sub("\n"," ",utfemail)
            match=re.match(r'.*Content\-Transfer\-Encoding:.*?(\<.*)$',utfemail,flags=re.IGNORECASE)
            content=re.sub(r'\<.*?\>'," ",re.sub(r'<style.*?>.*?<\/style>',"",match.group(1)))
        contents.append(content)
    return contents
def stripToText(string):
    return re.sub("-+","-",re.sub(" +"," ",re.sub(r'[^a-zA-Z0-9\' \.:/-]',"",re.sub(r'[\t\n\r]'," ",string))))
#for i in getPlainFromEmails(getEmailsIMAP("imap.gmail.com","mdr.brook@gmail.com","mmjixwvaxdwndlfc",ssl=True,count=10)):
#    print(stripToText(i))
#    print()
#    print()
