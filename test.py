import cv2
import numpy as np

def color_transfer(source, target):
    # 转换到 LAB 颜色空间
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    # 分离通道
    (lMeanSrc, aMeanSrc, bMeanSrc) = [source[..., i].mean() for i in range(3)]
    (lStdSrc, aStdSrc, bStdSrc) = [source[..., i].std() for i in range(3)]
    (lMeanTar, aMeanTar, bMeanTar) = [target[..., i].mean() for i in range(3)]
    (lStdTar, aStdTar, bStdTar) = [target[..., i].std() for i in range(3)]

    # 调整目标图像通道
    (l, a, b) = cv2.split(target)
    l = ((l - lMeanTar) * (lStdSrc / lStdTar)) + lMeanSrc
    a = ((a - aMeanTar) * (aStdSrc / aStdTar)) + aMeanSrc
    b = ((b - bMeanTar) * (bStdSrc / bStdTar)) + bMeanSrc
    transfer = cv2.merge([l, a, b])
    transfer = np.clip(transfer, 0, 255).astype("uint8")

    # 转回 BGR
    return cv2.cvtColor(transfer, cv2.COLOR_LAB2BGR)

# 示例
src = cv2.imread("source.jpg")  # 想要的色调
tgt = cv2.imread("target.png")  # 需要调整的图片
matched = color_transfer(src, tgt)
cv2.imwrite("matched.png", matched)
