# MVP Email Automation

最小化外贸开发信自动化工具 / Minimal Cold Email Automation Tool

---

## 背景 / Background

邮箱： 这个项目是针对腾讯企业邮箱接口设置的，部份参数需要去腾讯企业邮箱后台确认。

具体路径：设置 → 账户 → 客户端专用密码 → 生成新密码（新密码只显示一次，要保存好）

如果非腾讯企业邮箱，需要使用其他 SMTP 配置，详见下方「邮件服务商配置」。

隐私提示：这个项目的环境只适合在自己电脑上使用，账号、密码和客户信息都是未加密的，为了保护自己的信息安全，不要将正在使用的信息上传到公共平台。

---

## 项目文件 / Project Files

```
mvp-email-automation/
├── main.py              # 主程序 - 正式自动化发送邮件
├── 1_text_email.py      # 测试脚本 - 测试账号密码是否正确
├── data/
│   ├── email.html       # 邮件模板 - 可自定义内容
│   └── client_info.csv  # 联系人数据 - name, email 格式
├── venv/                # Python虚拟环境
└── requirements.txt    # 依赖列表
```

| 文件 | 说明                                    |
|------|---------------------------------------|
| `main.py` | 主程序，读取联系人 → 加载模板 → 发送邮件               |
| `1_text_email.py` | 测试脚本，先用这个验证邮箱能否发送                     |
| `data/email.html` | 邮件模板，用 `{name}` 作为收件人占位符              |
| `data/client_info.csv` | 联系人数据，包含 `name` 和 `email` 列 ，（必须作为表头） |

---

## 快速开始 / Quick Start

### 第一步：下载项目到电脑

打开终端（Mac：点击右上角放大镜，搜索「终端」；Windows：按 Win+R，输入「cmd」）

如果是 Windows 系统，先切换到 D 盘：
```bash
d:
```

下载 GitHub 项目：
```bash
git clone https://github.com/lsn1015/MVP-Email-Automation.git
```

进入项目文件夹：
```bash
cd mvp-email-automation
```

### 第二步：安装依赖

```bash
pip install requirements -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 第三步：测试账号

1. 用记事本或代码编辑器打开 `1_text_email.py`
2. 修改以下内容：
   - 第9行：`msg["From"] = "你的邮箱"`
   - 第10行：`msg["To"] = "你的收件邮箱"`
   - 第15行：`server.login("邮箱", "安全密码")`
3. 保存文件
4. 在终端运行：
```bash
python 1_text_email.py
```

如果显示「发送成功」，恭喜你，说明账号配置正确。

### 第四步：准备联系人

用 Excel 或记事本打开 `data/client_info.csv`，添加联系人：

```csv
name,email
John,john@example.com
Maria,maria@example.com
```

注意：`name` 列只填名字，不要填其他信息，因为邮件开头会自动写成「Dear John」。

### 第五步：自定义邮件模板

用浏览器打开 `data/email.html` 预览效果，用编辑器修改：
- 修改公司介绍、产品亮点等文字
- 修改图片链接（必须是公网可访问的URL，例如：在历史邮件里找到图片-鼠标右键点击-copy address）
- 修改签名为你的联系方式

### 第六步：配置发送参数

用编辑器打开 `main.py`，修改以下内容：

| 位置 | 修改内容 |
|------|----------|
| 第17行 | `EMAIL = "你的邮箱"` |
| 第18行 | `PASSWORD = "你的密码"` |
| 第21行 | `msg["Subject"] = "邮件标题"` |
| 第79行 | `file_path = "data/client_info.csv"` |

### 第七步：运行

```bash
python main.py
```

---

## 邮件服务商配置 / Email Service Configuration

默认配置为**腾讯企业邮箱**。以下是常用邮箱的 SMTP 配置：

### 腾讯企业邮箱 / Tencent Enterprise Email

```python
server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
```

### 常用邮箱 SMTP 配置 / Common SMTP Settings

| 邮箱服务 | SMTP服务器 | 端口 | 是否SSL |
|---------|-----------|------|--------|
| 腾讯企业邮箱 | smtp.exmail.qq.com | 465 | ✅ |
| QQ邮箱 | smtp.qq.com | 465 | ✅ |
| 163邮箱 | smtp.163.com | 465 | ✅ |
| Gmail | smtp.gmail.com | 587 | ✅ (TLS) |

### 修改 SMTP 配置

在 `main.py` 第26行修改：

```python
# 腾讯企业邮箱（默认）
server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)

# QQ邮箱
server = smtplib.SMTP_SSL("smtp.qq.com", 465)

# 163邮箱
server = smtplib.SMTP_SSL("smtp.163.com", 465)

# Gmail（可能需要开启低安全性应用）
server = smtplib.SMTP("smtp.gmail.com", 587)  # 注意：Gmail用SMTP而非SMTP_SSL
```

## 获取邮箱授权码 / Get Email Authorization Code

### 腾讯企业邮箱

1. 登录 [腾讯企业邮箱](https://exmail.qq.com/)
2. 进入 **设置** → **账户**
3. 找到 **IMAP/SMTP服务** → **生成授权码**
4. 使用授权码代替密码

### QQ邮箱

1. 登录 [QQ邮箱](https://mail.qq.com/)
2. 进入 **设置** → **账户**
3. 找到 **POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务**
4. 开启 **SMTP服务** → **生成授权码**

---

## 常见问题 / FAQ

### Q: 发送失败怎么办？

A: 1. 检查账号密码是否正确；2. 检查SMTP配置是否正确；3. 检查网络是否正常；4. 用 `1_text_email.py` 先测试单个邮件发送。

### Q: 图片无法显示？

A: 确保图片链接是公网可访问的完整URL，不能用本地文件路径。

### Q: 邮件被标记为垃圾邮件？

A: 1. 减少发送频率；2. 避免过多营销词汇；3. 邮件内容尽量个性化。

### Q: 如何更改发送延迟？

A: 修改 `main.py` 中的 `time.sleep(20)`，单位为秒。

---

**提示：首次使用建议先用 1-2 个联系人测试，确保配置正确后再批量发送。**

---

 ## 项目展望 / Project Roadmap                                                                                                                         
                                                                                                                                                        
  ### MVP（当前版本）                                                                                                                                   
                                                                                                                                                        
  最小化的邮件自动化工具，解决最基本的批量发送问题。                                                                                                    
                                                                                                                                                        
  ### v2.0：Agent 定制化邮件                                                                                                                            
                                                                                                                                                        
  下一步目标是变成 Agent 形态，根据客户职位定制化邮件内容：                                                                                             
                                                                                                                                                        
  - 读取联系人职位信息                                                                                                                                  
  - 结合职位生成针对性的邮件内容                                                                                                                        
  - 不同的职位发送不同版本的邮件                                                                                                                        
                                                                                                                                                        
  ### v3.0：RAG 垂类行业数据库                                                                                                                          
                                                                                                                                                        
  最终目标是结合 RAG（检索增强生成）做垂类行业的数据库型自动化背调：                                                                                    
                                                                                                                                                        
  - 建立行业产品知识库                                                                                                                                  
  - 自动收集目标客户背景信息                                                                                                                            
  - 生成带有行业洞察的个性化开发信                                                                                                                      
  - 从「大海捞针」变成「精准打击」                                                                                                                      
                                                                                                                                                        
  ---                                                                                                                                                   
                                                                                                                                                        
  ## 验证计划 / Validation Plan                                                                                                                         
                                                                                                                                                        
  记录个人开发效率与效果，按按月汇总分析：                                                                                                          
                                                                                                                                                        
  ### 每周记录                                                                                                                                          
                                                                                                                                                        
  - 发送数量 / 送达数量 / 回复数量                                                                                                                      
  - 平均回复率                                                                                                                                          
  - 花费时间（手动 vs 自动化）                                                                                                                          
                                                                                                                                                        
  ### 每月总结                                                                                                                                          
                                                                                                                                                        
  - 对比自动化前后的效率提升                                                                                                                            
  - 分析高回复率邮件的特征                                                                                                                              
  - 优化邮件模板和发送策略                                                                                                                              
                                                                                                                                                        
  ### 目标指标                                                                                                                                          
                                                                                                                                                        
  - 3个月内将开发信回复率提升至 5-10%                                                                                                                   
  - 节省 50% 的邮件撰写时间                                                                                                                             
- 建立可复用的邮件模板库

---

## 更新日志 / Changelog

### v1.1.0 (2026-04-15)

**重构项目结构，优化代码组织**

- 拆分 config/ 目录：邮件配置、SMTP 配置独立管理
- 拆分 core/ 目录：邮件发送器、模板管理器
- 拆分 tools/ 目录：联系人加载器、报告生成器
- main.py 从 332 行精简至 ~145 行，职责更清晰

**新增功能**

- 日志记录发送邮件状态（成功/失败），并生成报告
- 成功联系人记录：`logs/success_contacts_YYYYMMDD_HHMMSS.csv`
- 每日日志记录：`logs/all_emails_YYYYMMDD.log`
- 报告文件包含成功率、耗时等详细统计

**文件结构**

```
mvp-email-automation/
├── config/
│   ├── __init__.py
│   ├── email_config.py      # 邮箱账号、密码、主题
│   └── smtp_config.py       # SMTP 服务器配置
├── core/
│   ├── __init__.py
│   ├── sender.py            # 邮件发送核心
│   └── template.py          # 模板加载和渲染
├── tools/
│   ├── __init__.py
│   ├── contact_loader.py    # 读取联系人
│   └── report_generator.py  # 生成发送报告
├── logs/                    # 日志目录
├── data/
│   └── client_info.csv     # 联系人数据
├── main.py                 # 主入口
└── requirements.txt
```

### v1.0.0 (2026-04-13)

- 初始版本，邮件批量发送功能
