"""
邮件发送配置
"""
import os

EMAIL_CONFIG = {
    "address": os.getenv("EMAIL_ADDRESS", "your@email.com"),                                                                                          
    "password": os.getenv("EMAIL_PASSWORD", ""),                                                                                                      
    "subject": "...", 
}
