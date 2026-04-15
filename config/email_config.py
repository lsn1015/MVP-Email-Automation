"""
邮件发送配置
"""

EMAIL_CONFIG = {
    "address": os.getenv("EMAIL_ADDRESS", "your@email.com"),                                                                                          
    "password": os.getenv("EMAIL_PASSWORD", ""),                                                                                                      
    "subject": "...", 
}
