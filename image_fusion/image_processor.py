import os
from openai import OpenAI
from PIL import Image
import base64
import requests
from io import BytesIO
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

# 初始化OpenAI客户端，使用Mo平台API
client = OpenAI(
    api_key=os.environ['OPENAI_KEY'],  # 直接在这里填写你的API密钥
    base_url="https://open.momodel.cn/v1"  # Mo平台API基础URL
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

def encode_image_to_base64(image_path):
    """将图片转换为base64编码"""
    with Image.open(image_path) as image:
        if image.format != 'JPEG':
            image = image.convert('RGB')
        buffer = BytesIO()
        image.save(buffer, format='JPEG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

def generate_dalle_prompt(desc1, desc2, user_prompt):
    """使用GPT-4生成DALL-E提示词"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 文本处理使用gpt-4o
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的图像提示词专家，擅长将描述转换为DALL-E可用的精确提示词。请生成详细、富有创意且高质量的提示词。"
            },
            {
                "role": "user",
                "content": f"基于以下内容生成一个详细的DALL-E提示词：\n\n图片1描述：{desc1}\n\n图片2描述：{desc2}\n\n用户需求：{user_prompt}\n\n请生成一个能够很好融合这些元素的英文提示词。注重细节描述，包括风格、氛围、光线等要素。"
            }
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content

def calculate_output_size(width, height, max_width=1000):
    """计算输出尺寸，保持比例且宽度不超过max_width"""
    if width > max_width:
        ratio = max_width / width
        return (max_width, int(height * ratio))
    return (width, height)

@retry_with_backoff
def generate_image(prompt, original_image_path):
    """使用DALL-E生成图像，选择最接近原始比例的支持尺寸"""
    
    # 生成图片
    response = client.images.generate(
        model="dall-e-3",  # DALL-E 3
        prompt=prompt,
        size="1024x1024",
#         quality="hd",      # 最高质量
        style="vivid",     # 更生动的风格
        n=1,
    )
    
    return response.data[0].url

@retry_with_backoff
def save_image(url, output_path):
    """保存生成的图片"""
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)

def analyze_images_parallel(image1_path, image2_path):
    """并行分析两张图片"""
    with ThreadPoolExecutor(max_workers=2) as executor:
        # 提交两个任务
        future1 = executor.submit(get_image_description, image1_path)
        future2 = executor.submit(get_image_description, image2_path)
        
        try:
            # 等待两个任务完成
            desc1 = future1.result()
            desc2 = future2.result()
            return desc1, desc2
        except Exception as e:
            print(f"图片分析失败: {str(e)}")
            raise e

def process_images(image1_path, image2_path, user_prompt, output_path):
    """处理整个图像生成流程"""
    try:
        # 1. 并行获取两张图片的描述
        print("正在并行分析图片...")
        desc1, desc2 = analyze_images_parallel(image1_path, image2_path)
        
        # 2. 生成DALL-E提示词
        print("正在生成DALL-E提示词...")
        dalle_prompt = generate_dalle_prompt(desc1, desc2, user_prompt)
        
        # 3. 使用DALL-E生成图像
        print("正在生成最终图像...")
        try:
            image_url = generate_image(dalle_prompt, image1_path)
        except Exception as e:
            print(f"生成图像失败: {str(e)}")
            raise e
        
        # 4. 保存图像
        print("正在保存图像...")
        save_image(image_url, output_path)
        
        return {
            "status": "success",
            "image_url": image_url,
            "descriptions": {
                "image1": desc1,
                "image2": desc2,
                "dalle_prompt": dalle_prompt
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@retry_with_backoff
def get_image_description(image_path):
    """使用GPT-4 Vision获取图片描述"""
    base64_image = encode_image_to_base64(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "你是一个专业的图像分析专家，请尽可能详细和精确地描述图片。注意以下几点：\n1. 主体内容：准确描述主要对象的位置、大小、形状和颜色\n2. 细节特征：描述重要的细节，如纹理、材质、光影效果\n3. 空间关系：说明各个元素之间的位置关系\n4. 环境背景：描述场景的整体氛围和环境特征\n5. 风格特点：分析图片的艺术风格或拍摄风格"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请对这张图片进行极其详细的分析和描述，包括：\n1. 图片的主要内容是什么？\n2. 主体的具体特征如何（颜色、形状、材质等）？\n3. 主体的位置在哪里，与其他元素的关系如何？\n4. 背景环境有什么特点？\n5. 光线和氛围如何？\n6. 有什么独特或显著的细节？\n\n请尽可能精确地描述每个细节，不要遗漏任何重要信息。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    
    return response.choices[0].message.content