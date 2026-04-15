# -*- coding: utf-8 -*-
"""
邮件自动化发送主程序
"""

import time
import logging
from datetime import datetime
from pathlib import Path

from config import EMAIL_CONFIG
from core import EmailSender, TemplateManager
from tools import ContactLoader, ReportGenerator


# =============================
# 日志配置
# =============================
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f'all_emails_{datetime.today().strftime("%Y%m%d")}.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('email_automation')


# =============================
# 主流程
# =============================
def main():
    file_path = "data/client_info.csv"

    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("开始批量发送邮件")
    logger.info(f"联系人文件: {file_path}")
    logger.info(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)

    # 加载联系人
    loader = ContactLoader()
    contacts = loader.load(file_path)

    if not contacts:
        logger.error("没有找到有效的联系人，程序退出")
        return

    logger.info(f"成功加载 {len(contacts)} 个联系人")

    # 初始化组件
    sender = EmailSender()
    template_manager = TemplateManager()
    report_gen = ReportGenerator()

    try:
        template = template_manager.load()
    except Exception as e:
        logger.error(f"无法加载邮件模板: {e}")
        return

    # 记录发送结果
    success_list = []
    failed_list = []

    # 循环发送
    for idx, contact in enumerate(contacts, 1):
        name = contact["name"]
        email = contact["email"]

        logger.info(f"\n[{idx}/{len(contacts)}] 正在处理: {name} ({email})")

        # 生成邮件内容
        try:
            email_content = template_manager.render(template, name=name)
        except Exception as e:
            logger.error(f"生成邮件内容失败: {name}, 错误: {e}")
            failed_list.append({
                'name': name,
                'email': email,
                'error': f"内容生成失败: {e}",
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            continue

        # 发送邮件
        success, error = sender.send(email, email_content)

        if success:
            logger.info(f"✅ 发送成功 → {name} ({email})")
            success_list.append({
                'name': name,
                'email': email,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        else:
            logger.error(f"❌ 发送失败 → {name} ({email}): {error}")
            failed_list.append({
                'name': name,
                'email': email,
                'error': error,
                'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })

        # 防封间隔
        if idx < len(contacts):
            logger.info("等待30秒后发送下一封...")
            time.sleep(30)

    # 生成报告
    report = report_gen.generate(success_list, failed_list, start_time)

    # 打印摘要
    print("\n" + "=" * 60)
    print("发送完成！")
    print(f"✅ 成功: {report['success']}")
    print(f"❌ 失败: {report['failed']}")
    print(f"📊 成功率: {report['success_rate']}")
    print(f"📁 日志目录: {log_dir.absolute()}")
    print("=" * 60)

    if failed_list:
        print("\n失败的联系人（前5个）:")
        for failed in failed_list[:5]:
            print(f"  - {failed['name']} ({failed['email']})")
        if len(failed_list) > 5:
            print(f"  ... 还有 {len(failed_list) - 5} 个失败")


# =============================
# 启动
# =============================
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("\n⚠️ 程序被用户中断")
        print("\n程序已停止")
    except Exception as e:
        logger.error(f"程序运行出错: {e}")
        print(f"\n❌ 程序出错: {e}")
