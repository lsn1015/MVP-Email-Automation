
# 先用这个程序跑个测试，验证一下是否可以发送

import smtplib
from email.mime.text import MIMEText

msg = MIMEText("Hello, this is a test email") # 邮件内容
msg["Subject"] = "Test"  # 邮件subject
msg["From"] = "name@companyname.com" # ⚠️ 需要更改！： 发出邮箱： 开发用邮箱
msg["To"] = "self@qq.com"  # ️⚠️ 需要更改： 接受邮箱 ： 最好用自己的邮箱先测试

server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465) # 不要改
server.set_debuglevel(1) # 不要改
server.ehlo()  # 不要改
server.login("name@companyname.com", "mima") #  ⚠️ 账号（邮箱地址）， 密码（生成密码）
server.send_message(msg)
server.quit()

print("发送成功") # 打印日志