# MultiUserWalletBot 完整部署包

## 包含文件
- encrypt_wallets.py ：加密用户钱包配置。
- decrypt_wallets.py ：解密钱包配置。
- bot.py ：主程序，微信企业群机器人接口。
- wallets.enc ：需自行生成加密钱包文件（见说明）。

## 使用说明

### 1. 配置钱包加密
1. 修改 encrypt_wallets.py 中 wallets 字典，添加所有用户的钱包地址和私钥。
2. 设置环境变量（16位密钥）：
   - Linux/macOS: export WALLET_SECRET_KEY=1234567890abcdef
   - Windows PowerShell: $env:WALLET_SECRET_KEY="1234567890abcdef"
3. 运行 python encrypt_wallets.py 生成 wallets.enc 文件。

### 2. 运行机器人
- 确保 bot.py、decrypt_wallets.py 和 wallets.enc 在同一目录。
- 修改 bot.py 中 WALLET_SECRET_KEY 为你的密钥。
- 运行 python bot.py 启动服务器，默认监听5000端口。

### 3. 微信群使用说明
- 群内发送消息格式：
  - 绑定Webhook：绑定Webhook https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxx
  - 查询代币信息：直接发送代币合约地址
- 机器人自动识别链（ETH/BSC/SOL），返回币种详情及买卖示范信息。

## 安全建议
- 私钥文件已加密，密钥请妥善保存，不要硬编码在公共代码。
- 生产环境建议使用HTTPS和身份验证保护接口。
- 定期更新钱包密钥，避免风险。

## 依赖
- Python 3.7+
- Flask
- requests
- pycryptodome (`pip install pycryptodome flask requests`)

---

以上只是无聊写了个Bot，里面代码买卖不是很完善，如果造成损失，自行承担！如果你是开发人员，可以自行完善代码自行部署！谢谢。
祝你部署顺利！需要打包文件请告诉我。


### 打包步骤

1.把上面4个代码文件分别保存为：

encrypt_wallets.py
decrypt_wallets.py
bot.py
README.md

2.用命令行进入该目录，运行以下命令打包zip：

zip MultiUserWalletBot.zip encrypt_wallets.py decrypt_wallets.py bot.py README.md

3.上传到你的云服务器，安装依赖：

pip install pycryptodome flask requests


4.设置环境变量（16位密钥）：

export WALLET_SECRET_KEY=1234567890abcdef

（Windows PowerShell 请用 $env:WALLET_SECRET_KEY="1234567890abcdef"）

5.运行：

python encrypt_wallets.py
python bot.py


如果你是开发，可以增加一个判断处理一下以下情况，企业微信封号发不出信息的时候判断一下。以当前买入价格自动出售！就算封号，bot自动出售！代码需要完善的东西很多，没时间去完善！

