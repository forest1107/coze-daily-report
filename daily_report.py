import requests
import json
requests.packages.urllib3.disable_warnings()

# ====================== 替换成新创建的参数 ======================
COZE_TOKEN = "pat_4TcOw8JB27lv5H92umYAfTAoarw56ch1hIBvXO0aw0GoUcfyR8qoIUaV5EdlaGoz"  # 必须是刚创建的
COZE_BOT_ID = "7609251421359898676"
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/31ef233d-cdbe-46f3-a97b-c1ce8e3d2b5f"
# ======================================================================

def get_coze_report():
    api_url = f"https://www.coze.cn/api/v3/chat?bot_id={COZE_BOT_ID}"
    # 严格校验令牌格式（避免手动输入错误）
    if not COZE_TOKEN.startswith("pat_"):
        return "错误：Coze令牌格式错误，必须以pat_开头"
    
    headers = {
        "Authorization": f"Bearer {COZE_TOKEN.strip()}",  # 自动去空格
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    payload = {
        "conversation_id": "daily_report_001",
        "user": {"id": "test_user_123"},
        "query": "生成今日AI日报，3条核心资讯，每条不超过80字，简洁易懂",
        "stream": False,
        "temperature": 0.7
    }

    try:
        res = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        res.raise_for_status()
        result = res.json()

        if result.get("messages") and len(result["messages"]) > 0:
            content = result["messages"][-1]["content"].strip().replace("\n\n", "\n")
            return content
        else:
            return f"Coze返回无内容：{json.dumps(result, ensure_ascii=False)[:200]}"

    except requests.exceptions.HTTPError as e:
        error_msg = f"Coze API错误：{str(e)} | 响应：{res.text[:200]}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"调用失败：{str(e)}"
        print(error_msg)
        return error_msg

def send_to_feishu(content):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "msg_type": "text",
        "content": {"text": f"【今日AI日报】\n{content}"}
    }

    try:
        res = requests.post(
            FEISHU_WEBHOOK,
            headers=headers,
            data=json.dumps(data, ensure_ascii=False),
            timeout=10,
            verify=False
        )
        print(f"飞书推送结果：{res.text}")
    except Exception as e:
        print(f"飞书推送失败：{str(e)}")

if __name__ == "__main__":
    report_content = get_coze_report()
    send_to_feishu(report_content)
    print("\n===== 脚本执行完成 =====")
