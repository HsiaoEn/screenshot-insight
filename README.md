# Screenshot Insight

Screenshot Insight 是一個基於 Python 的開源工具，利用 Windows 系統內建的截圖工具與 GPT-4o 模型的先進 OCR 與圖像分析能力，讓使用者只需按下 Print Screen 鍵，即可捕捉螢幕上指定的區域，並獲得該區域內文字與其他視覺元素的詳細描述。

## 特色

- **簡單的截圖捕捉：**  
  按下 Print Screen 鍵即可啟動 Windows 系統截圖工具，讓你選取所需的截圖區域。

- **自動圖像擷取：**  
  截圖完成後，工具會自動從剪貼簿讀取圖片並進行後續處理。

- **圖像預處理：**  
  擷取的圖片會先轉換為灰階，再依原始比例縮放。

- **先進的 OCR 與圖像描述：**  
  利用 GPT-4o 模型，不僅能準確提取圖片中的文字，還能對包含圖像結構和其他視覺元素的截圖給出詳盡描述。

### 依賴套件

使用 pip 安裝所需套件：

```sh
pip install pillow requests openai python-dotenv keyboard
