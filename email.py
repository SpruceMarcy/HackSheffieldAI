import imaplib
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
print(getEmailsIMAP("imap.gmail.com","mdr.brook@gmail.com","oivbfyidlycjgkus",ssl=True))
