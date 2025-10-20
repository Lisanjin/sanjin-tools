import comfy.model_management
import torch

class ImageToLatent():
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("LATENT",)
    FUNCTION = "image2latent"
    CATEGORY = "sanjin/ImageToLatent"

    def __init__(self):
        self.device = comfy.model_management.intermediate_device()

    @classmethod
    def INPUT_TYPES(s):
        return { "required":  { "images": ("IMAGE",), } }

    
    def image2latent(self, images):
        image_shape = images.shape
        

        height = image_shape[1]
        width = image_shape[2]
        
        print(f"width: {width}, height: {height}")
        return self.create_empty_latent(width, height)


    def create_empty_latent(self,width,height):
        latent = torch.zeros([1, 4, height // 8, width // 8], device=self.device)
        return ({"samples":latent},)