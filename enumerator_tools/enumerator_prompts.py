class EnumeratorPrompt:

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "index": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff, "control_after_generate": True,}),
                "text": ("STRING", {
                    "multiline": True, 
                    "default": ""
                }),
            }
        }

    def select_prompt(self, text, index):
        prompt_list = text.split("\n")
        return (prompt_list[index],)
    
    OUTPUT_NODE = True
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
 
    FUNCTION = "select_prompt"
 
    CATEGORY = "sanjin/EnumeratorPrompt"
 