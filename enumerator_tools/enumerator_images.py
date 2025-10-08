import os
import torch # ComfyUI 依赖 torch，我们可以用它来加载图片并转换为 tensor
from PIL import Image, ImageOps, ImageSequence
import numpy as np
import folder_paths
import node_helpers

# 定义一个支持的图片文件扩展名列表
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.bmp', '.gif')

class EnumeratorImages:

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
 
    FUNCTION = "select_image"
 
    CATEGORY = "sanjin/EnumeratorImages"

    @classmethod
    def INPUT_TYPES(s):
        input_dir = folder_paths.get_input_directory()
        return {
            "required": {
                # 将 "text" 输入改为 "folder_path"，使其更具描述性
                "folder_path": ("STRING", {
                    "multiline": False,
                    "default": input_dir # 提示用户输入文件夹路径
                }),
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True,}),
            }
        }


    def select_image(self, folder_path, index):
        file_list = os.listdir(folder_path)
        image_list = []
        for file in file_list:
            if file.endswith(IMAGE_EXTENSIONS):
                image_list.append(file)
                
        return self.load_image(folder_path + "/" + image_list[index])
    
    def load_image(self, image):
        image_path = folder_paths.get_annotated_filepath(image)

        img = node_helpers.pillow(Image.open, image_path)

        output_images = []
        output_masks = []
        w, h = None, None

        excluded_formats = ['MPO']

        for i in ImageSequence.Iterator(img):
            i = node_helpers.pillow(ImageOps.exif_transpose, i)

            if i.mode == 'I':
                i = i.point(lambda i: i * (1 / 255))
            image = i.convert("RGB")

            if len(output_images) == 0:
                w = image.size[0]
                h = image.size[1]

            if image.size[0] != w or image.size[1] != h:
                continue

            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if 'A' in i.getbands():
                mask = np.array(i.getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            elif i.mode == 'P' and 'transparency' in i.info:
                mask = np.array(i.convert('RGBA').getchannel('A')).astype(np.float32) / 255.0
                mask = 1. - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64,64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1 and img.format not in excluded_formats:
            output_image = torch.cat(output_images, dim=0)
        else:
            output_image = output_images[0]

        return (output_image,)

