from .enumerator_tools.enumerator_prompts import EnumeratorPrompt
from .enumerator_tools.enumerator_images import EnumeratorImages
from .string_tools.regex_processing import RegexProcessing
from .latent_tools.latent_presets import LatentPresets
from .latent_tools.image_to_latent import ImageToLatent


NODE_CLASS_MAPPINGS = {
    "enumerator_prompts": EnumeratorPrompt,
    "enumerator_images": EnumeratorImages,
    "regex_processing": RegexProcessing,
    "latent_presets": LatentPresets,
    "image_to_latent": ImageToLatent
}
 
NODE_DISPLAY_NAME_MAPPINGS = {
    "enumerator_prompts": "枚举prompt",
    "enumerator_images": "枚举图片",
    "regex_processing": "正则处理",
    "latent_presets": "latent预设",
    "image_to_latent": "创建图片尺寸latent"
}

all = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']