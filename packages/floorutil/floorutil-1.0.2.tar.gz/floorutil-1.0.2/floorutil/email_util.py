import yagmail

# 指定收件人发送邮件
def send_email():
    yag = yagmail.SMTP(user="xuzhili@znds.com", password="presentAND323232", host="smtp.znds.com")
    yag.send(to="lintao@znds.com", subject="邮件批量发送测试", contents=["Hello need not to answer"])
    return

def main():
    print("test send_email")

if __name__ == "__main__":
    send_email()
    print("send an email")
