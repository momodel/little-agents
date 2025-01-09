import replicate
import os
from PIL import Image
import requests
from io import BytesIO
import random
import string
import json

if not os.environ.get('REPLICATE_API_TOKEN'):
    os.environ['REPLICATE_API_TOKEN'] = 'your key'

if not os.environ.get('OPENAI_KEY'):
    os.environ['OPENAI_KEY'] = 'your key'

OPENAI_KEY = os.environ['OPENAI_KEY']

def get_random_filename(extension=".png"):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16)) + extension

def download_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

def save_image_from_url(url, filename):
    image = download_image(url)
    image.save(filename)


def handle(conf):
    """
    该方法是部署之后，其他人调用你的服务时候的处理方法。
    请按规范填写参数结构，这样我们就能替你自动生成配置文件，方便其他人的调用。
    范例：
    params['key'] = value # value_type: str # description: some description
    value_type 可以选择：img, video, audio, str, int, float, [int], [str], [float]
    参数请放到params字典中，我们会自动解析该变量。
    """

    img_path=conf['图片']
    input={
        "image": 'https://momodel.cn/pyapi/file/temp_file/' + img_path.replace('/tmp/', ''),
        "prompt": "During the day, it snowed and the snow was falling, covering the objects in the picture.",
        "negative_prompt":"(deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime:1.4), text, close up, cropped, out of frame, worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck."

    }

    output = replicate.run(
        "usamaehsan/controlnet-1.1-x-realistic-vision-v2.0:51778c7522eb99added82c0c52873d7a391eecf5fcc3ac7856613b7e6443f2f7",
        input=input
    )   

    output_url = output
    output_filename = get_random_filename()
    save_image_from_url(output_url, output_filename)
    return {'入冬后': output_filename}