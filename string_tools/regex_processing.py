import re


class RegexProcessing:

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("STRING",)
    FUNCTION = "processing"
    CATEGORY = "sanjin/RegexProcessing"


    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {
                    "multiline": True, 
                    "default": ""
                }),
                "regex_pattern": ("STRING", { # 正则表达式输入
                    "multiline": False,
                    "default": ""
                }),
                "operation": (["delete", "replace"],), # 操作选项：删除或替换
                "replacement_text": ("STRING", { # 替换内容输入
                    "multiline": False,
                    "default": ""
                }),
            }
        }

    def processing(self, text, regex_pattern, operation, replacement_text):
        if not regex_pattern:
            return (text,)

        # 添加 flags=re.M 来确保 ^ 匹配每一行的开头
        if operation == "delete":
            processed_text = re.sub(regex_pattern, "", text, flags=re.M)
        elif operation == "replace":
            processed_text = re.sub(regex_pattern, replacement_text, text, flags=re.M)
        else:
            processed_text = text

        return (processed_text,)
 

 # 示例使用 (在ComfyUI中运行时不需要这些)
if __name__ == "__main__":
    processor = RegexProcessing()

    # 示例1: 删除所有非字母数字字符
    text1 = "Hello, World! 123"
    regex1 = r'[^a-zA-Z0-9]'
    result1 = processor.processing(text1, regex1, "delete", "")
    print(f"Original: '{text1}', Processed (delete non-alphanumeric): '{result1[0]}'")

    # 示例2: 将所有数字替换为 'X'
    text2 = "Item A: 123, Item B: 456"
    regex2 = r'\d+'
    result2 = processor.processing(text2, regex2, "replace", "X")
    print(f"Original: '{text2}', Processed (replace digits with 'X'): '{result2[0]}'")

    # 示例3: 删除所有空格
    text3 = "This is a test string."
    regex3 = r'\s'
    result3 = processor.processing(text3, regex3, "delete", "")
    print(f"Original: '{text3}', Processed (delete spaces): '{result3[0]}'")