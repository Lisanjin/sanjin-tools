import cv2
import numpy as np
import torch

def color_transfer(source, target):
    source = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
    target = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

    (lMeanSrc, aMeanSrc, bMeanSrc) = [source[..., i].mean() for i in range(3)]
    (lStdSrc, aStdSrc, bStdSrc) = [source[..., i].std() for i in range(3)]
    (lMeanTar, aMeanTar, bMeanTar) = [target[..., i].mean() for i in range(3)]
    (lStdTar, aStdTar, bStdTar) = [target[..., i].std() for i in range(3)]

    (l, a, b) = cv2.split(target)
    l = ((l - lMeanTar) * (lStdSrc / lStdTar)) + lMeanSrc
    a = ((a - aMeanTar) * (aStdSrc / aStdTar)) + aMeanSrc
    b = ((b - bMeanTar) * (bStdSrc / bStdTar)) + bMeanSrc
    transfer = cv2.merge([l, a, b])
    transfer = np.clip(transfer, 0, 255).astype("uint8")

    return cv2.cvtColor(transfer, cv2.COLOR_LAB2BGR)

class ColorSync():
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("Synced Image",)

    FUNCTION = "color_sync"
    CATEGORY = "sanjin/ColorSync"


    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "source_image": ("IMAGE",),
                "target_image": ("IMAGE",),
            }
        }
    
    def color_sync(self, source_image, target_image):
        src = (source_image[0].cpu().numpy() * 255).clip(0, 255).astype(np.uint8)
        tgt = (target_image[0].cpu().numpy() * 255).clip(0, 255).astype(np.uint8)

        src_bgr = cv2.cvtColor(src, cv2.COLOR_RGB2BGR)
        tgt_bgr = cv2.cvtColor(tgt, cv2.COLOR_RGB2BGR)

        result_bgr = color_transfer(src_bgr, tgt_bgr)

        result_rgb = cv2.cvtColor(result_bgr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
        result_rgb = np.expand_dims(result_rgb, axis=0)

        return (torch.from_numpy(result_rgb),)

