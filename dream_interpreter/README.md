# AI 智能解梦

一个专业的梦境分析工具，结合心理学原理深度解读梦境，并通过 AI 艺术创作将梦境场景可视化呈现。

## 功能特点

- 🧠 专业的心理学角度分析
- 🔍 多维度深入解读梦境含义
- 🎨 梦境场景艺术可视化
- 💭 个性化反思建议
- 🔁 内置错误重试机制
- 🎯 精准的象征意义解析

## 技术实现

- 使用 GPT-4 进行专业梦境分析
- 使用 GPT-4 生成优化的 DALL-E 提示词
- 使用 DALL-E 3 生成梦境场景
- 基于 Mo 平台的 API 服务

## 使用方法

1. 准备环境：
   ```bash
   pip install -r requirements.txt
   ```

2. 设置环境变量：
   ```bash
   export OPENAI_KEY='your-api-key'
   ```

3. 调用服务：
   ```python
   from dream_app import handle
   
   result = handle({
       '梦境描述': '详细的梦境内容描述'
   })
   
   print(result['解梦报告'])  # 输出解梦分析
   print(result['梦境图像'])  # 输出生成的图片路径
   ```

## 输入参数

- `梦境描述`：详细描述梦境内容，包括场景、人物、情节和感受

## 输出结果

- `解梦报告`：专业的梦境心理分析报告，包含多个维度的深度解读
- `梦境图像`：AI 生成的梦境场景艺术呈现

## 分析维度

1. 概述：总体解读，揭示潜意识情绪和心理状态
2. 主题概述：分析梦的主题和现实关联
3. 关键符号：解读梦中关键符号的象征意义
4. 情感景观：分析梦中的情绪氛围
5. 潜在含义：揭示深层心理动机
6. 反思点：提供反思性问题
7. 总结：总结启示和建议

## 示例

```python
conf = {
    '梦境描述': '我梦见自己在一个古老的图书馆里，书架高耸入云。突然，所有的书开始发光，像萤火虫一样飘在空中。我感到既惊讶又平静。'
}
result = handle(conf)
```

## 注意事项

1. 梦境描述越详细越好
2. 包含个人感受和情绪体验
3. 建议记录梦醒后的第一印象
4. API 密钥需要有足够的配额

## 依赖项

- openai==1.3.5
- Pillow==10.1.0
- requests==2.31.0 