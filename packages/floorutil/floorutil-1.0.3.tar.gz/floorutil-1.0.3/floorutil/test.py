from floorutil import email_util as el

if __name__ == '__main__':
    send_email = el.SendMail
    send_email.send_mail(send_email,"zhili", "li", "test", "hello", "xuzhili@znds.com", "password",
                         "1150713603@qq.com")
