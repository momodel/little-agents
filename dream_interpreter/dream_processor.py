import os
from openai import OpenAI
import time
import random

# 初始化OpenAI客户端
client = OpenAI(
    api_key=os.environ['OPENAI_KEY'],
    base_url="https://open.momodel.cn/v1"
)

def retry_with_backoff(func, max_retries=3, initial_delay=1):
    """带有退避策略的重试机制"""
    def wrapper(*args, **kwargs):
        delay = initial_delay
        last_exception = None
        
        for retry in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                print(f"尝试 {retry + 1}/{max_retries} 失败: {str(e)}")
                if retry < max_retries - 1:
                    sleep_time = delay + random.uniform(0, 1)
                    print(f"等待 {sleep_time:.1f} 秒后重试...")
                    time.sleep(sleep_time)
                    delay *= 2
        
        raise last_exception
    return wrapper

@retry_with_backoff
def analyze_dream(dream_description):
    """分析梦境内容"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """你是一位专业的梦境心理分析专家，擅长从心理学角度解读梦境。请按以下结构解析梦境：

1. 概述：总体解读，揭示潜意识情绪和心理状态
2. 主题概述：分析梦的主题和现实关联
3. 关键符号：解读梦中关键符号的象征意义
4. 情感景观：分析梦中的情绪氛围
5. 潜在含义：揭示深层心理动机
6. 反思点：提供反思性问题
7. 总结：总结启示和建议"""
            },
            {
                "role": "user",
                "content": dream_description
            }
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content

@retry_with_backoff
def generate_dream_image(dream_description, dream_analysis):
    """生成梦境场景图像"""
    # 先生成图像提示词
    prompt_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """你是一位专业的DALL-E提示词专家。请将用户的梦境描述转换为详细的图像生成提示词。
注意：
1. 提示词应该富有艺术感和想象力
2. 包含场景、氛围、光线等细节
3. 使用简洁的英文描述
4. 确保提示词能捕捉梦境的超现实感"""
            },
            {
                "role": "user",
                "content": f"梦境描述：{dream_description}\n\n心理分析：{dream_analysis}\n\n请生成一个能够捕捉这个梦境场景的DALL-E提示词。"
            }
        ],
        max_tokens=200
    )
    
    image_prompt = prompt_response.choices[0].message.content
    
    # 使用生成的提示词创建图像
    response = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        quality="standard",
        style="vivid",
        n=1,
    )
    
    return response.data[0].url

def process_dream(dream_description):
    """处理整个解梦流程"""
    try:
        # 1. 分析梦境
        print("正在分析梦境...")
        dream_analysis = analyze_dream(dream_description)
        
        # 2. 生成梦境图像
        print("正在生成梦境图像...")
        try:
            image_url = generate_dream_image(dream_description, dream_analysis)
            
            return {
                "status": "success",
                "dream_analysis": dream_analysis,
                "image_url": image_url
            }
        except Exception as e:
            # 如果图像生成失败，仍然返回解梦分析
            error_message = str(e)
            if "content_policy_violation" in error_message:
                error_message = "您的梦境描述包含了一些敏感内容，无法生成图像。但这不影响解梦分析的结果。"
            
            return {
                "status": "error",
                "message": error_message,
                "dream_analysis": dream_analysis
            }
        
    except Exception as e:
        error_message = str(e)
        if "content_policy_violation" in error_message:
            error_message = "您的梦境描述包含了一些敏感内容，请调整描述后重试。"
            
        return {
            "status": "error",
            "message": error_message
        } 