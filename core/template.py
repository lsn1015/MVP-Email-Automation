"""
邮件模板管理
"""

from pathlib import Path


class TemplateManager:
    """邮件模板管理器"""

    def __init__(self, template_path: str = "tools/2test_email.html"):
        self.template_path = Path(template_path)

    def load(self) -> str:
        """加载模板"""
        with open(self.template_path, "r", encoding="utf-8") as f:
            return f.read()

    def render(self, template: str, **kwargs) -> str:
        """
        渲染模板
        :param template: 模板内容
        :param kwargs: 替换变量，如 name="张三"
        :return: 渲染后的内容
        """
        content = template
        for key, value in kwargs.items():
            content = content.replace(f"{{{key}}}", str(value))
        return content
