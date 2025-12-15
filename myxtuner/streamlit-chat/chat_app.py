# 多轮对话
from openai import OpenAI
# 定义多轮对话方法
def run_chat_session():
    # 初始化客户端（指向本地模型服务）
    client = OpenAI(
        base_url="http://localhost:23333/v1",  # 你的模型服务地址
        api_key="suibianxie"  # 可以随便填，仅作占位符
    )
    # 初始化对话历史
    chat_history = []
    # 启动对话循环
    while True:
        # 获取用户输入
        user_input = input("用户: ")
        if user_input.lower() == "exit":
            print("退出对话。")
            break
        # 更新对话历史（添加用户输入）
        chat_history.append({"role": "user", "content": user_input})
        # 调用模型回答
        try:
            chat_completion = client.chat.completions.create(
                messages=chat_history,
                model="/root/autodl-fs/xtuner_merged/qwen1_5_1_8b_chat_qlora_alpaca_e3/iter_2000_hf_merged"  # 模型名称需与服务中注册的一致（例如：qwen1_5_1_8b_chat）
            )
            # 获取最新回答
            model_response = chat_completion.choices[0]
            print("AI:", model_response.message.content)
            # 更新对话历史（添加AI模型的回复）
            chat_history.append({"role": "assistant", "content": model_response.message.content})
        except Exception as e:
            print("发生错误：", e)
            break
if __name__ == '__main__':
    run_chat_session()