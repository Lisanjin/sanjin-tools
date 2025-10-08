import os
import json
import torch
import comfy.model_management

class LatentPresets():
    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("LATENT",)
    FUNCTION = "create_empty_latent_from_name"
    CATEGORY = "sanjin/LatentPresets"


    def __init__(self):
        self.device = comfy.model_management.intermediate_device()
    
    @classmethod
    def INPUT_TYPES(s):
        presets_folder = os.path.dirname(os.path.abspath(__file__))
        with open(presets_folder + "/presets.json", "r", encoding="utf-8") as f:
            presets = json.load(f)

        latent_presets = presets["latent"]
        presets_names = [p["name"] for p in latent_presets]
        return {
            "required":{
                "presets_name": (presets_names,),
                "invert_dimensions": ("BOOLEAN", {
                    "default": False, 
                    "label_on": "宽高反转", 
                    "label_off": "正常宽高"
                })
            }
        }
    
    def create_empty_latent_from_name(self, presets_name, invert_dimensions):
        presets_folder = os.path.dirname(os.path.abspath(__file__))
        with open(presets_folder + "/presets.json", "r", encoding="utf-8") as f:
            presets = json.load(f)

        latent_presets = presets["latent"]
        latent_preset = next((p for p in latent_presets if p["name"] == presets_name), None)
        w = latent_preset["width"]
        h = latent_preset["height"]

        if invert_dimensions:
            w, h = h, w

        return self.create_empty_latent(w,h)

    def create_empty_latent(self,width,height):
        latent = torch.zeros([1, 4, height // 8, width // 8], device=self.device)
        return ({"samples":latent},)