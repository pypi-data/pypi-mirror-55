Help on module email_util:

NAME
    email_util

CLASSES
    builtins.object
        SendMail
    
    class SendMail(builtins.object)
     |  实用该类可向指定邮箱地址发送邮件
     |  
     |  Methods defined here:
     |  
     |  parse_options(self)
     |      解析外部输入数据
     |      -f from_name
     |      -t to_name
     |      -s subject
     |      -c content
     |      -p pwd
     |      -a to_addr
     |      :return:
     |  
     |  send_mail(self, from_name, to_name, subject, content, from_addr, pwd, to_addr)
     |      发送邮件
     |      :param from_name: 发送方名字，数组类型，可指定多个
     |      :param to_name: 收件人名字，数组类型，可指定多个
     |      :param subject: 邮件主题
     |      :param content: 邮件内容
     |      :param from_addr: 发送方邮箱地址，数组类型，可指定多个
     |      :param pwd: 发送方邮箱密码
     |      :param to_addr: 发送方邮箱地址，数组类型，可指定多个
     |      :return:
     |  
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |  
     |  __dict__
     |      dictionary for instance variables (if defined)
     |  
     |  __weakref__
     |      list of weak references to the object (if defined)

FILE
    d:\pythoncode\floorutil\floorutil\email_util.py


