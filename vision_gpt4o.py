import os
import time
import base64
import requests
import io
from PIL import ImageGrab, Image, ImageOps
import openai
from dotenv import load_dotenv
import keyboard  # 偵測鍵盤按鍵

# 讀取 .env 中的 API 金鑰
load_dotenv()
api_key = os.getenv('openai_apikey')
if not api_key:
    raise ValueError("API key 未設定，請檢查 .env 檔案。")
openai.api_key = api_key

# 確保 images 資料夾存在
if not os.path.exists('images'):
    os.makedirs('images')

def encode_image(image):
    """將 PIL Image 轉成 JPEG 格式並編碼成 base64 字串"""
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return encoded

def resize_image(image, max_size=512):
    """等比例縮放圖片，使寬或高不超過 max_size"""
    width, height = image.size
    scale = min(max_size / width, max_size / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

def preprocess_image(image):
    """
    預處理圖片：
    1. 轉為灰階
    2. 等比例縮放圖片，使得寬或高不超過 512 像素
    """
    processed = image.convert("L")
    processed = resize_image(processed, max_size=512)
    return processed

def analyze_image(image):
    """
    呼叫 GPT-4o 模型對圖片進行分析。
    image 為預處理後的 PIL Image 物件。
    """
    encoded_image = encode_image(image)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "gpt-4o",
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text":  "Please carefully examine the attached image. The image may contain both text and other visual elements or structured content. Provide a detailed and comprehensive description of the overall content of the screenshot, including any visible text, layout, and key visual features. Your response should clearly summarize what is present in the image without adding extraneous commentary."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                            "detail": "low"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    return response.json()

def wait_for_system_snip():
    """
    偵測使用者按下 Print Screen 鍵後，等待系統將截圖存入剪貼簿，
    然後從剪貼簿取得圖片。
    注意：此方式需要 Windows 已將 Print Screen 設為啟動系統截圖工具，
    並且截圖完成後圖片會複製到剪貼簿。
    """
    print("請按下 Print Screen 鍵以啟動 Windows 截圖工具...", flush=True)
    while True:
        if keyboard.is_pressed("print_screen"):
            print("偵測到 Print Screen 鍵，等待系統截圖...", flush=True)
            # 給系統截圖工具一些時間讓使用者選取範圍並將圖片存入剪貼簿
            time.sleep(1.5)
            # 嘗試從剪貼簿取得圖片，若尚未複製成功則輪詢
            timeout = 10  # 最長等待 10 秒
            start_time = time.time()
            image = ImageGrab.grabclipboard()
            while image is None and (time.time() - start_time) < timeout:
                time.sleep(0.5)
                image = ImageGrab.grabclipboard()
            if image is None:
                print("未偵測到剪貼簿中的圖片，請確認已使用系統截圖工具完成截圖。", flush=True)
            else:
                print("成功取得剪貼簿中的圖片！", flush=True)
                return image
        time.sleep(0.1)

if __name__ == "__main__":
    while True:
        # 等待使用者使用系統截圖工具截圖
        image = wait_for_system_snip()
        if image is not None:
            # 對圖片進行預處理 (灰階轉換 + 等比例縮放)
            processed_image = preprocess_image(image)
            # 可選：將預處理後的圖片存檔以供參考
            processed_image.save("images/processed_image.jpg", "JPEG")
            # 呼叫 GPT-4o 模型進行圖片推論
            try:
                result = analyze_image(processed_image)
                answer = result['choices'][0]['message']['content']
                print("模型回應：", answer, flush=True)
            except Exception as e:
                print("分析圖片時發生錯誤：", e, flush=True)
        print("請再次按下 Print Screen 鍵以進行新的截圖...", flush=True)
