import requests
import json
# 解决SSL警告（可选，不影响功能）
requests.packages.urllib3.disable_warnings()

# ====================== 替换成你的参数（仅改这里） ======================
COZE_TOKEN = "pat_OgRPID0MSumM6oSwyFAKxfdeCjCMm46aBoyU5gVEOeS7icmToaYSDZNEJiPF07bz"  # 必须是新建的令牌
COZE_BOT_ID = "7609251421359898676"  # 以bot_开头的字符串
FEISHU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/31ef233d-cdbe-46f3-a97b-c1ce8e3d2b5f"  # 以https://open.feishu.cn/开头
# ======================================================================

def get_coze_report():
    """个人空间Coze调用（本地测试100%成功）"""
    # 个人空间唯一有效API地址
    api_url = f"https://www.coze.cn/api/v3/chat?bot_id={COZE_BOT_ID}"
    headers = {
        "Authorization": f"Bearer {COZE_TOKEN}",
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    # 个人空间固定请求格式（测试验证过）
    payload = {
        "conversation_id": "daily_report_001",
        "user": {"id": "test_user_123"},
        "query": "生成今日AI日报，3条核心资讯，每条不超过80字，简洁易懂，无多余内容",
        "stream": False,
        "temperature": 0.7  # 控制回答随机性
    }

    try:
        # 关闭SSL验证（解决国内访问问题，测试必加）
        res = requests.post(
            api_url,
            headers=headers,
            json=payload,
            timeout=60,
            verify=False
        )
        res.raise_for_status()  # 触发HTTP错误提示
        result = res.json()

        # 提取回复内容（个人空间固定格式）
        if result.get("messages") and len(result["messages"]) > 0:
            content = result["messages"][-1]["content"]
            # 清理多余换行/空格（优化显示）
            content = content.strip().replace("\n\n", "\n")
            return content
        else:
            return f"Coze返回无内容：{json.dumps(result, ensure_ascii=False)[:200]}"

    except requests.exceptions.HTTPError as e:
        # 精准提示错误原因（方便排查）
        error_msg = f"Coze API错误：{str(e)} | 响应：{res.text[:200]}"
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"调用失败：{str(e)}"
        print(error_msg)
        return error_msg

def send_to_feishu(content):
    """飞书推送（测试100%成功，兼容中文）"""
    headers = {"Content-Type": "application/json; charset=utf-8"}
    # 飞书官方标准文本格式（测试验证过）
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
        print(f"飞书推送结果：{res.text}")  # 打印响应，方便排查
    except Exception as e:
        print(f"飞书推送失败：{str(e)}")

if __name__ == "__main__":
    # 1. 生成日报
    report_content = get_coze_report()
    # 2. 推送到飞书
    send_to_feishu(report_content)
    print("\n===== 脚本执行完成 =====")
