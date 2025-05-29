import json
import requests
from decrypt_wallets import decrypt_wallet_config
from flask import Flask, request, jsonify

app = Flask(__name__)

# 读取钱包配置（请部署时填写正确密钥）
WALLET_SECRET_KEY = "1234567890abcdef"
wallets = decrypt_wallet_config("wallets.enc", WALLET_SECRET_KEY)

# 群聊Webhook管理，格式：{group_id: webhook_url}
group_webhooks = {}

def detect_chain(ca):
    """简单识别链类型："""
    if ca.startswith("0x") and len(ca) == 42:
        return "ETH"
    if len(ca) == 44:  # Solana地址长度示例
        return "SOL"
    if ca.startswith("0x") and len(ca) == 42:
        return "BSC"
    return "UNKNOWN"

def query_token_info(ca, chain):
    """模拟API请求，返回币种信息"""
    # 这里需要你接入真实API
    return {
        "name": "FRAME",
        "symbol": "FRAME",
        "chain": chain,
        "market_cap": "$462.9K",
        "pool_value": "$134.4K",
        "sol_pool": "375.06",
        "dev_holding": "0%",
        "top10_percent": "31.26%",
        "twitter": True,
        "telegram": False,
        "website": True,
        "community_heat": "19个群讨论29次"
    }

def format_message(info):
    """格式化推送消息"""
    msg = (
        f"${info['name']} ({info['symbol']}) —— {info['chain']}\\n"
        f"当前市值: {info['market_cap']}\\n"
        f"池子: {info['pool_value']} / SOL池: {info['sol_pool']}\\n"
        f"开发者当前持有量: {info['dev_holding']}\\n"
        f"Top10 占比: {info['top10_percent']}\\n"
        f"🔗 推特{'✅' if info['twitter'] else '❌'} "
        f"电报{'✅' if info['telegram'] else '❌'} "
        f"官网{'✅' if info['website'] else '❌'}\\n"
        f"👥 社区热度: {info['community_heat']}\\n\\n"
        f"买入: 2 SOL  卖出: 2 SOL\\n"
        f"交易签名: 示例签名abc123..."
    )
    return msg

def send_to_wechat(webhook, content):
    """调用企业微信Webhook接口发送消息"""
    data = {
        "msgtype": "text",
        "text": {"content": content}
    }
    response = requests.post(webhook, json=data)
    return response.status_code == 200

@app.route("/wechat_bot", methods=["POST"])
def wechat_bot():
    data = request.json
    user = data.get("user")  # 微信用户名
    group_id = data.get("group_id")
    msg_text = data.get("msg")

    if msg_text.startswith("绑定Webhook"):
        # 用户群聊绑定Webhook示例格式：绑定Webhook https://qyapi.weixin.qq 填写自己企业微信机器人的webhook
        parts = msg_text.split()
        if len(parts) == 2:
            group_webhooks[group_id] = parts[1]
            return jsonify({"msg": "Webhook绑定成功，群聊独立配置已生效"})
        else:
            return jsonify({"msg": "绑定Webhook格式错误，请输入：绑定Webhook webhook_url"})

    if group_id not in group_webhooks:
        return jsonify({"msg": "请先绑定Webhook，格式：绑定Webhook webhook_url"})

    webhook = group_webhooks[group_id]

    # 用户发送代币合约地址
    ca = msg_text.strip()
    chain = detect_chain(ca)
    if chain == "UNKNOWN":
        return jsonify({"msg": "无法识别合约地址所属链，请确认后重试"})

    info = query_token_info(ca, chain)
    content = format_message(info)

    # 发送到企业微信群
    success = send_to_wechat(webhook, content)
    if success:
        return jsonify({"msg": "信息已发送到群"})
    else:
        return jsonify({"msg": "发送失败，请检查Webhook配置"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
