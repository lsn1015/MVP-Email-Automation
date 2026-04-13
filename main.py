import pandas as pd
import smtplib
import time
from email.mime.text import MIMEText



# =============================
#  邮件发送
# =============================

def send_email(name, email, content):
    EMAIL = "EMAIL" #  ⚠️ 请修改！： 开发邮箱地址
    PASSWORD= "PASSWORD" #  ⚠️ 请修改！： 安全密码

    msg = MIMEText(content, "html", "utf-8")
    msg["Subject"] = f"xxx Production Facility"  #  ⚠️ 请修改！： 开发邮件标题subject
    msg["From"] = EMAIL
    msg["To"] = email

    try:
        server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
        server.set_debuglevel(1)
        server.ehlo()
        server.login(EMAIL, PASSWORD)
        server.send_message(msg)
        server.quit()

        print(f"✅ 已发送 → {name} ({email})")

    except Exception as e:
        print(f"❌ 发送失败 → {name}: {e}")

# =============================
# 邮件模版
# =============================
def load_template():
    with open("data/email.html", "r", encoding="utf-8") as f:  #  ⚠️ 邮件模版
        return f.read()

# ===== 2. 替换变量 =====
def render_template(template, name):
    return template.replace("{name}", name).replace("{image_cid}", "cid:image1")


# =============================
# 支持 Excel / CSV  格式文件
# =============================
def load_contacts(file_path):
    if file_path.endswith(".xlsx"):
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)

    df.columns = [col.lower() for col in df.columns]

    contacts = []
    for _, row in df.iterrows():
        name = row.get("name")
        email = row.get("email")

        if pd.notna(name) and pd.notna(email):
            contacts.append({
                "name": name,
                "email": email
            })

    return contacts


# =============================
# 🚀 主流程（你控制循环）
# =============================
def main():
    file_path = f"data/client_info.csv"  #  ⚠️ 请修改！： 联系人client_info的储存路径（cvs/xlsx)

    contacts = load_contacts(file_path)

    print(f"📊 共加载 {len(contacts)} 个联系人\n")

    for contact in contacts:
        name = contact["name"]
        email = contact["email"]

        print(f"\n🐱 正在处理: {name}")

        # 1️⃣ 生成邮件
        content = load_template()
        email_content = render_template(content, name)

        print("📨 正在发送邮件...")

        # 2️⃣ 发送邮件
        send_email(name, email, email_content)

        # ⚠️ 非常重要！： 延迟发送设置，单位为“秒”，发送太频繁会被封号，建议设置20秒/封
        time.sleep(20)


# =============================
# ▶️ 启动
# =============================
if __name__ == "__main__":
    main()