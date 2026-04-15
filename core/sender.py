"""
邮件发送核心模块
"""

import smtplib
import traceback
from email.mime.text import MIMEText
from typing import Optional

from config import EMAIL_CONFIG, SMTP_CONFIG


class EmailSender:
    """邮件发送器"""

    def __init__(self):
        self.email = EMAIL_CONFIG["address"]
        self.password = EMAIL_CONFIG["password"]
        self.subject = EMAIL_CONFIG["subject"]
        self.smtp_host = SMTP_CONFIG["host"]
        self.smtp_port = SMTP_CONFIG["port"]
        self.use_ssl = SMTP_CONFIG["use_ssl"]

    def send(self, to_email: str, content: str) -> tuple[bool, Optional[str]]:
        """
        发送邮件
        :param to_email: 收件人邮箱
        :param content: 邮件内容（HTML）
        :return: (是否成功, 错误信息)
        """
        msg = MIMEText(content, "html", "utf-8")
        msg["Subject"] = self.subject
        msg["From"] = self.email
        msg["To"] = to_email

        try:
            if self.use_ssl:
                server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_host, self.smtp_port)

            server.set_debuglevel(0)
            server.ehlo()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()

            return True, None

        except smtplib.SMTPServerDisconnected as e:
            return False, f"服务器断开连接: {e}"

        except smtplib.SMTPAuthenticationError as e:
            return False, f"认证失败，请检查邮箱密码: {e}"

        except smtplib.SMTPException as e:
            return False, f"SMTP错误: {e}"

        except Exception as e:
            error_msg = str(e)
            if "UNEXPECTED_EOF" in error_msg or "SSLEOFError" in error_msg:
                return False, f"SSL连接错误: {error_msg}"
            return False, f"发送失败: {error_msg}"
