import requests
import json

# ====================== 替换成你的参数 ======================
COZE_TOKEN = "pat_OgRPID0MSumM6oSwyFAKxfdeCjCMm46aBoyU5gVEOeS7icmToaYSDZNEJiPF07bz"
COZE_BOT_ID = "7609251421359898676"
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/31ef233d-cdbe-46f3-a97b-c1ce8e3d2b5f"
# ===========================================================

def get_coze_report():
    """调用Coze API生成AI日报"""
    url = "https://api.coze.cn/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {COZE_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "bot_id": COZE_BOT_ID,
        "user_id": "your_user_id",  # 随便填，比如你的手机号
        "query": "帮我汇总今天的AI资讯，包括36氪、虎嗅、IT之家、InfoQ的内容，每条不超过50字，分来源列出",
        "stream": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        # 提取生成的内容
        content = result["choices"][0]["message"]["content"]
        return content
    except Exception as e:
        return f"生成日报失败：{str(e)}"

def send_to_feishu(content):
    """推送到飞书"""
    url = FEISHU_WEBHOOK
    headers = {"Content-Type": "application/json"}
    payload = {
        "msg_type": "text",
        "content": {"text": f"【今日AI日报】\n{content}"}
    }
    try:
        requests.post(url, headers=headers, json=payload, timeout=10)
        print("推送飞书成功")
    except Exception as e:
        print(f"推送飞书失败：{str(e)}")

if __name__ == "__main__":
    # 1. 生成日报
    report = get_coze_report()
    print("生成的日报：", report)
    # 2. 推送到飞书
    send_to_feishu(report)
