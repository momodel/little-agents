import os
import random
import string
from PIL import Image
import requests
from io import BytesIO
from image_processor import process_images

if not os.environ.get('OPENAI_KEY'):
    os.environ['OPENAI_KEY'] = 'your key'

def get_random_filename(extension=".png"):
    """生成随机文件名"""
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)) + extension

def download_image(url):
    """从URL下载图片"""
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def save_image_from_url(url, filename):
    """保存URL图片到文件"""
    image = download_image(url)
    image.save(filename)

def handle(conf):
    """
    处理图像融合请求的主函数
    
    参数说明：
    conf['图片1'] = value # value_type: str # description: 第一张图片的路径，作为主要风格来源
    conf['图片2'] = value # value_type: str # description: 第二张图片的路径，作为融合元素来源
    conf['融合描述'] = value # value_type: str # description: 描述如何将两张图片的元素融合
    
    返回值：
    {'生成图片': 生成的图片路径}
    """
    
    # 获取输入参数
    img1_path = conf['图片1']
    img2_path = conf['图片2']
    prompt = conf['融合描述']
    
    # 转换Mo平台的临时文件路径到完整URL
    img1_url = 'https://momodel.cn/pyapi/file/temp_file/' + img1_path.replace('/tmp/', '')
    img2_url = 'https://momodel.cn/pyapi/file/temp_file/' + img2_path.replace('/tmp/', '')
    
    # 下载图片到本地临时文件
    temp_img1 = get_random_filename()
    temp_img2 = get_random_filename()
    save_image_from_url(img1_url, temp_img1)
    save_image_from_url(img2_url, temp_img2)
    
    # 生成输出文件名
    output_filename = get_random_filename()
    
    try:
        # 处理图片
        result = process_images(temp_img1, temp_img2, prompt, output_filename)
        
        # 清理临时文件
        os.remove(temp_img1)
        os.remove(temp_img2)
        
        if result['status'] == 'success':
            return {'生成图片': output_filename}
        else:
            raise Exception(result['message'])
            
    except Exception as e:
        # 清理临时文件
        if os.path.exists(temp_img1):
            os.remove(temp_img1)
        if os.path.exists(temp_img2):
            os.remove(temp_img2)
        if os.path.exists(output_filename):
            os.remove(output_filename)
            
        raise Exception(f"处理失败: {str(e)}")

# 测试代码
if __name__ == "__main__":
    # 测试配置
    test_conf = {
        '图片1': '/path/to/image1.jpg',
        '图片2': '/path/to/image2.jpg',
        '融合描述': '雷峰塔戴着围巾'
    }
    
    try:
        result = handle(test_conf)
        print("生成成功:", result)
    except Exception as e:
        print("生成失败:", str(e)) 