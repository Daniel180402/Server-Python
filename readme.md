# **AI Server Setup Guide**

This guide provides step-by-step instructions to set up and run the AI server.

---

## **Prerequisites**

### **1. Install Python**
- Ensure you have **Python 3.7 or later** installed on your system.
- [Download Python here](https://www.python.org/downloads/).
- Follow [this guide](https://packaging.python.org/en/latest/tutorials/installing-packages/) for installing and using `pip`.

### **2. Install Ollama**
- Download and install Ollama from [ollama.com](https://ollama.com/).
- **Important:** Pull the `llama3` model for the server to function. In a terminal, run:   
    ```ollama pull llama3```

You can use [this guide](https://medium.com/@gabrielrodewald/running-models-with-ollama-step-by-step-60b6f6125807) to help you install and use Ollama.

### **3. Install FFmpeg**
FFmpeg is required for handling audio files.  
- [Download FFmpeg here](https://ffmpeg.org/download.html) or install it using Chocolatey (in this case use the command ```choco install ffmpeg```)

You can use [this guide](https://phoenixnap.com/kb/ffmpeg-windows) to help you install FFmpeg on Windows.

## **Setting Up the Environment**

### **Install Required Python Packages**
Run the following command to install necessary dependencies:
    ```pip install flask gtts SpeechRecognition ollama```

## **Running the Server**
Start the server by running:
   python python_server.py
   
Once the server is running, it will be accessible at:
http://localhost:5000
