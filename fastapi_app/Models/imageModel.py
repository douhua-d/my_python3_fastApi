import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models

# 这个脚本是用 ResNet18 预训练模型对图片进行物体分类的标准范例。
# 只要换成你自己的图片，就能预测出属于 ImageNet 1000 类别中的哪一类。
# 你的脚本能做什么？
# 输入一张图片（如猫、狗、钟表、飞机等常见物体）
# 输出模型认为这是什么类别（比如 "tabby cat"、"wall clock"、"airliner" 等）
# 注意：
# 只能识别 ImageNet 1000 类中的物体，不能识别自定义类别。
# 

# 加载预训练模型
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
model.eval()

# 图像预处理
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],  # ImageNet 的标准均值和方差
        std=[0.229, 0.224, 0.225]
    )
])

# 载入图像并转换
img = Image.open("001.jpg")
img_t = transform(img)
batch_t = torch.unsqueeze(img_t, 0)  # 扩展维度

# 模型预测
with torch.no_grad():
    out = model(batch_t)

# 获取预测结果
_, index = torch.max(out, 1)

# 加载标签（可选）
import json
import urllib.request
url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
labels = urllib.request.urlopen(url).read().decode("utf-8").splitlines()
print(f"预测结果: {labels[index.item()]}")
