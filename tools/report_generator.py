"""
发送报告生成器
"""

import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class ReportGenerator:
    """发送报告生成器"""

    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

    def generate(self, success_list: List[Dict], failed_list: List[Dict], start_time: datetime) -> Dict:
        """
        生成发送报告
        :param success_list: 成功列表
        :param failed_list: 失败列表
        :param start_time: 开始时间
        :return: 报告数据
        """
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        total = len(success_list) + len(failed_list)

        report = {
            'total': total,
            'success': len(success_list),
            'failed': len(failed_list),
            'success_rate': f"{len(success_list) / total * 100:.2f}%" if total > 0 else "0%",
            'duration': f"{duration:.2f}秒",
            'start_time': start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'failed_list': failed_list
        }

        self._save_report(report, success_list, failed_list, start_time)

        return report

    def _save_report(self, report: Dict, success_list: List[Dict], failed_list: List[Dict], start_time: datetime):
        """保存报告到文件"""
        # 保存文本报告
        report_file = self.log_dir / f'report_{start_time.strftime("%Y%m%d_%H%M%S")}.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=" * 60 + "\n")
            f.write("邮件发送报告\n")
            f.write("=" * 60 + "\n")
            f.write(f"开始时间: {report['start_time']}\n")
            f.write(f"结束时间: {report['end_time']}\n")
            f.write(f"总耗时: {report['duration']}\n")
            f.write(f"总联系人数: {report['total']}\n")
            f.write(f"成功: {report['success']}\n")
            f.write(f"失败: {report['failed']}\n")
            f.write(f"成功率: {report['success_rate']}\n")
            f.write("\n失败列表:\n")
            for failed in report['failed_list']:
                f.write(f"  - {failed['name']} ({failed['email']}): {failed['error']}\n")

        # 保存失败列表为CSV
        if failed_list:
            failed_df = pd.DataFrame(failed_list)
            failed_csv = self.log_dir / f'failed_contacts_{start_time.strftime("%Y%m%d_%H%M%S")}.csv'
            failed_df.to_csv(failed_csv, index=False, encoding='utf-8-sig')

        # 保存成功列表为CSV
        if success_list:
            success_df = pd.DataFrame(success_list)
            success_csv = self.log_dir / f'success_contacts_{start_time.strftime("%Y%m%d_%H%M%S")}.csv'
            success_df.to_csv(success_csv, index=False, encoding='utf-8-sig')
