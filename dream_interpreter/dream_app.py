import os
import random
import string
import requests
from io import BytesIO
from PIL import Image
from dream_processor import process_dream

if not os.environ.get('OPENAI_KEY'):
    os.environ['OPENAI_KEY'] = 'your key'

def get_random_filename(extension=".png"):
    """生成随机文件名"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)) + extension

def save_image_from_url(url, filename):
    """保存URL图片到文件"""
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(filename)

def handle(conf):
    """
    处理解梦请求的主函数
    
    参数说明：
    conf['梦境描述'] = value # value_type: str # description: 用户的梦境描述
    
    返回值：
    {
        '解梦报告': 心理分析报告,
        '梦境图像': 生成的图像路径
    }
    """
    
    # 获取输入参数
    dream_description = conf['梦境描述']
    
    try:
        # 处理梦境
        result = process_dream(dream_description)
        
        if result['status'] == 'success':
            # 保存生成的图像
            image_filename = get_random_filename()
            save_image_from_url(result['image_url'], image_filename)
            
            return {
                '解梦报告': result['dream_analysis'],
                '梦境图像': image_filename
            }
        else:
            # 处理失败，返回错误信息和错误图片
            # 如果有解梦分析，返回错误信息和解梦分析
            if 'dream_analysis' in result:
                return {
                    '解梦报告': f"[图像生成失败：{result['message']}]\n\n{result['dream_analysis']}",
                    '梦境图像': './error.png'
                }
            # 如果完全失败，只返回错误信息
            return {
                '解梦报告': result['message'],
                '梦境图像': './error.png'
            }
            
    except Exception as e:
        # 发生异常，返回错误信息和错误图片
        return {
            '解梦报告': f"解梦过程中出现错误：{str(e)}",
            '梦境图像': './error.png'
        }

# 测试代码
if __name__ == "__main__":
    # 测试配置
    test_conf = {
        '梦境描述': '我梦见自己在一个古老的图书馆里，书架高耸入云。突然，所有的书开始发光，像萤火虫一样飘在空中。我感到既惊讶又平静。'
    }
    
    result = handle(test_conf)
    print("解梦报告:", result['解梦报告'])
    print("梦境图像:", result['梦境图像']) 