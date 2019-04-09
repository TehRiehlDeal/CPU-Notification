def readEmails():
    server = imaplib.IMAP4_SSL('theriehldeal.com', 993)
    server.login(credentials.username, credentials.password)
    server.select('Inbox')

    result, data = server.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    newResult, newData = server.fetch(str(latest_email_id), "(RFC822)")
    msg = email.message_from_bytes(newData[0][1])
    print(msg['content-type'])
    """
    for i in range(latest_email_id, first_email_id, -1):
        result, data = server.fetch(str(i), '(RFC822)')

        print(data)          """
