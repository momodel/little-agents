# AI 创意工具集

这是一个基于 OpenAI API 的创意工具集合，包含两个独立的 AI 应用：图像创意融合和智能解梦。两个应用都部署在 Mo 平台上，提供简单易用的 API 接口。

## 项目结构

```
.
├── image_fusion/           # 图像创意融合项目
│   ├── app.py             # 应用入口
│   ├── app_spec.yml       # API 配置
│   ├── image_processor.py # 图像处理核心逻辑
│   └── README.md          # 项目说明
│
└── dream_interpreter/     # 智能解梦项目
    ├── dream_app.py      # 应用入口
    ├── dream_app.yml     # API 配置
    ├── dream_processor.py# 解梦处理核心逻辑
    └── README.md         # 项目说明
```

## 图像创意融合

一个强大的 AI 工具，能够智能地将两张图片的元素融合在一起，创造出独特的艺术作品。

### 主要特点
- 保持主图片的风格和氛围
- 智能融入第二张图片的元素
- 支持自然语言描述融合方式
- 并行处理提升效率

[详细说明](./image_fusion/)

## 智能解梦

一个专业的梦境分析工具，结合心理学原理深度解读梦境，并通过 AI 艺术创作将梦境场景可视化呈现。

### 主要特点
- 专业的心理学角度分析
- 多维度深入解读
- 梦境场景可视化
- 提供个性化建议

[详细说明](./dream_interpreter/)

## 技术栈

- OpenAI GPT-4/GPT-4 Vision
- DALL-E 3
- Python 3.8+
- Mo 平台 API

## 环境要求

1. Python 3.8 或更高版本
2. OpenAI API 密钥
3. Mo 平台账号

## 快速开始

1. 克隆仓库：
   ```bash
   git clone [repository-url]
   cd ai-creative-tools
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 设置环境变量：
   ```bash
   export OPENAI_KEY='your-api-key'
   ```

4. 选择项目并按照各自的 README 说明使用

## 注意事项

1. API 密钥安全：
   - 不要在代码中硬编码 API 密钥
   - 使用环境变量或配置文件管理密钥

2. 资源使用：
   - 注意 API 调用频率限制
   - 监控 API 使用配额
   - 合理使用并行处理功能

3. 错误处理：
   - 所有 API 调用都有重试机制
   - 详细的错误日志记录
   - 友好的错误提示

## 贡献指南

欢迎提交 Issue 和 Pull Request 来帮助改进项目。

## 许可证

MIT License 