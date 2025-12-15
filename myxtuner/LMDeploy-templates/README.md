## 模型转换
模型训练后会自动保存成 PTH模型（例如 iter_2000.pth，如果使用了 DeepSpeed，则将会是一个文件夹），
我们需要利用 xtuner convert pth_to_hf 将其转换为 HuggingFace模型，以便于后续使用。具体命令为：
```shell
xtuner convert pth_to_hf ${FINETUNE_CFG} ${PTH_PATH} ${SAVE_PATH}
```
- 执行命令
```shell
xtuner convert pth_to_hf /root/xtuner/myxtuner/qwen1_5_1_8b_chat_qlora_alpaca_e3_20251215.py  /root/autodl-fs/xtuner_out/qwen1_5_1_8b_chat_qlora_alpaca_e3/iter_2000.pth /root/autodl-fs/xtuner_convert/qwen1_5_1_8b_chat_qlora_alpaca_e3/iter_2000_hf
```


## 模型合并
如果使用了 LoRA/QLoRA微调，则模型转换后将得到 adapter参数，而并不包含原 LLM参数。如果您期望获得合并后的模型权重（例如用于后续评测），那么可以利用 xtuner convert merge：
```shell
xtuner convert merge ${LLM} ${LLM_ADAPTER} ${SAVE_PATH}
```
- 执行命令
```shell
xtuner convert merge  /root/autodl-fs/base_model/Qwen1.5-1.8B-Chat  /root/autodl-fs/xtuner_convert/qwen1_5_1_8b_chat_qlora_alpaca_e3/iter_2000_hf  /root/autodl-fs/xtuner_merged/qwen1_5_1_8b_chat_qlora_alpaca_e3/iter_2000_hf_merged
```

## LMDeploy部署
在使用 CLI 工具时，可以通过 --chat-template 传入自定义对话模板，比如：
```shell
lmdeploy serve api_server /root/autodl-fs/xtuner_merged/qwen1_5_1_8b_chat_qlora_alpaca_e3/iter_2000_hf_merged --chat-template chat_template.json
```

## 启动本地模型服务（示例：使用 streamlit）
```shell
streamlit run chat_app.py
```