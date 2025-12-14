## 使用modelscope命令下载模型，进度条都不动就是下载完了：
```shell
modelscope download --model 'Qwen/Qwen1.5-1.8B-Chat' --local_dir '/mnt/e/base_model/Qwen1.5-1.8B-Chat'
```

```shell
pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
pip config set install.trusted-host mirrors.aliyun.com
```

```shell
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn
```

```shell
pip config set global.index-url https://pypi.mirrors.ustc.edu.cn/simple/
pip config set install.trusted-host mirrors.ustc.edu.cn
```


## 首先需要拉取XTuner代码并安装依赖：
```shell
# 创建conda环境
conda deactivate
conda create -n xtuner-env python=3.10 -y
conda activate xtuner-env

# 克隆XTuner仓库
git clone https://github.com/InternLM/xtuner.git
cd xtuner

# 安装依赖（此步骤耗时较长） 
# 新文档
pip install -e '.[all]'

# 旧文档，目前安装旧文档操作
pip install -U 'xtuner[deepspeed]' #  通过 pip 安装（推荐方案 a）  成功
pip install -e '.[deepspeed]' # 源码安装，好像有点问题
```
- 验证安装
```shell
xtuner list-cfg
```

## 使用ModelScope下载预训练模型：
```shell
 modelscope download --model 'Qwen/Qwen1.5-1.8B-Chat' --local_dir '/mnt/e/base_model/Qwen1.5-1.8B-Chat'
```

## 修改配置文件中的关键参数：[qwen1_5_1_8b_chat_qlora_alpaca_e3.py](qwen1_5_1_8b_chat_qlora_alpaca_e3.py)
```shell
### PART 1中
# 预训练模型存放的位置
pretrained_model_name_or_path = '/mnt/e/base_model/Qwen1.5-1.8B-Chat'  # 基座模型路径
# 微调数据存放的位置
data_files = '/home/wenguoli/xtuner/myxtuner/data/target_data.json'

# 训练参数设置
max_length = 512  # 训练中最大的文本长度
batch_size = 4    # 每一批训练样本的大小
max_epochs = 3000    # 最大训练轮数

# Save
save_steps = 100
save_total_limit = 2  # Maximum checkpoints to keep (-1 means unlimited)

# 验证数据
evaluation_inputs = [
    '只剩一个心脏了还能活吗？',
    '爸爸再婚，我是不是就有了个新娘？',
    '樟脑丸是我吃过最难吃的硬糖有奇怪的味道怎么还有人买',
    '马上要上游泳课了，昨天洗的泳裤还没干，怎么办',
    '我只出生了一次，为什么每年都要庆生'
]

### PART 3中 (path="json")
dataset = dict(type=load_dataset, path="json", data_files=data_files)
dataset_map_fn = None
```

- 指定从某个位置继续训练（可选）
```shell
# load from which checkpoint
load from =
"/mnt/e/xtuner/qwen1_5_1_8b_chat_qlora_alpaca_e3/iter_100.pth"
```

- 需要安装低版本的torch，执行以下依赖包，否则会报错
```shell
bitsandbytes==0.45.0
datasets>=3.2.0
einops
loguru
mmengine==0.10.6
openpyxl
peft>=0.14.0
scikit-image
scipy
SentencePiece
tiktoken
torch==2.5.1
torchvision==0.20.1
transformers==4.57.3
transformers_stream_generator==0.0.5
```
- 20251213 新的github代码中，不升级transformers 这个最新，会报错

## 单卡微调（单机单卡）-- 目前运行这个成功
```shell
xtuner train --work-dir /mnt/e/xtuner/qwen1_5_1_8b_chat_qlora_alpaca_e3 /home/wenguoli/xtuner/myxtuner/qwen1_5_1_8b_chat_qlora_alpaca_e3.py 
```

## 多卡微调（单机多卡）
```shell
NPROC_PER_NODE=2 xtuner train --work-dir /mnt/e/xtuner/qwen1_5_1_8b_chat_qlora_alpaca_e3 /home/wenguoli/xtuner/myxtuner/qwen1_5_1_8b_chat_qlora_alpaca_e3.py --deepspeed deepspeed_zero2
```





