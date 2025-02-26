# Screenshot Insight

Screenshot Insight is a Python-based open-source tool that leverages Windows' built-in snipping tool and the advanced OCR/visual analysis capabilities of the GPT-4o model. With just a press of the Print Screen key, you can capture a specific area of your screen and receive a detailed description of its content—including both text and other visual elements.

## Features

- **Easy Screenshot Capture:**  
  Press the Print Screen key to trigger the Windows snipping tool and select the desired area.

- **Automatic Image Retrieval:**  
  The tool automatically fetches the captured image from the clipboard once you finish selecting the area.

- **Image Preprocessing:**  
  The captured image is converted to grayscale and resized proportionally (ensuring that the maximum width or height does not exceed 512 pixels) to optimize it for analysis.

- **Advanced OCR and Visual Analysis:**  
  Leverages the GPT-4o model to extract and describe all visible text as well as other key visual elements present in the screenshot.

- **Lightweight & Open Source:**  
  Built using Python and various popular libraries, making it easy to install, customize, and extend.

## Installation

### Prerequisites

- **Python 3.8+**  
- **Windows OS:** Ensure that the Print Screen key is configured to launch the snipping tool.
- **Git:** (Optional) For version control.

### Dependencies

Install the required packages using pip:

```sh
pip install pillow requests openai python-dotenv keyboard
