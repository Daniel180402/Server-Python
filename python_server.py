import ollama
from flask import Flask, request, jsonify
from gtts import gTTS
import os
import base64
import speech_recognition as sr

# Rules for the AI's response generation
RULES = (
    "1. Respond in Italian"
    "2. Use a maximum of 50 words"
    "3. Be comprehensible to children"
    "4. Avoid lists"
    "5. Maintain a formal and respectful tone"
    "6. Do not use exclamations like 'Oh, oh!' or 'Haha'"
)

app = Flask(__name__)

def get_ai_response(user_input: str) -> str:
    # Sends the user's input to the AI model and collects the response in a streamed manner
    response_tokens = ollama.chat(
        model='llama3',
        messages=[
            {'role': 'system', 'content': RULES},
            {'role': 'user', 'content': user_input}
        ],
        stream=True
    )

    response_text = ""
    for tok in response_tokens:
        content = tok['message']['content']
        response_text += content
    return response_text

def generate_tts_audio(response_text: str, filename: str) -> str:
    # Converts text into an audio file using Google Text-to-Speech (gTTS)
    tts = gTTS(text=response_text, lang="it", slow=False)
    tts.save(filename)
    return filename

@app.route('/voice_input', methods=['POST'])
def handle_voice_input():
    # Handles voice input, converts it to text, queries the AI, and returns TTS audio of the response
    temp_path = "temp_audio.wav"
    audio_filename = "response_audio.mp3"

    try:
        if 'audio' not in request.files:
            return jsonify({"error": "No audio file uploaded"}), 400

        # Save the uploaded audio file temporarily
        audio_file = request.files['audio']
        audio_file.save(temp_path)

        # Convert the saved audio file into text using Google Speech Recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(temp_path) as source:
            audio_data = recognizer.record(source)

        try:
            # Try to recognize the audio in Italian
            recognized_text = recognizer.recognize_google(audio_data, language="it-IT")
        except sr.UnknownValueError:
            # Handle cases where speech could not be understood
            recognized_text = "Sorry, I didn't understand what you said. Could you repeat?"
        except sr.RequestError as e:
            # Handle errors related to the speech recognition service
            recognized_text = f"STT service error: {e}"

        # Get the AI response for the recognized text
        response = get_ai_response(recognized_text)

        # Generate TTS audio for the AI's response
        generate_tts_audio(response, audio_filename)

        # Read the TTS audio file and convert it to Base64 for returning to the client
        with open(audio_filename, "rb") as af:
            audio_base64 = base64.b64encode(af.read()).decode("utf-8")

        return jsonify({
            "recognized_text": recognized_text,
            "response": response,
            "audio_base64": audio_base64
        })

    finally:
        # Cleanup temporary files to ensure no persistent storage
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(audio_filename):
            os.remove(audio_filename)

@app.route('/get_response', methods=['POST'])
def get_text_response():
    # Handles text input, queries the AI, and returns TTS audio of the response
    temp_audio_filename = "response_audio.mp3"

    try:
        # Parse the input data to get the user's text input
        data = request.get_json()
        if not data or 'user_input' not in data:
            return jsonify({"error": "Missing 'user_input' in request body"}), 400

        user_input = data['user_input']

        # Query the AI for a response
        response = get_ai_response(user_input)

        # Generate TTS audio for the AI's response
        generate_tts_audio(response, temp_audio_filename)

        # Read the TTS audio file and convert it to Base64 for returning to the client
        with open(temp_audio_filename, "rb") as af:
            audio_base64 = base64.b64encode(af.read()).decode("utf-8")

        return jsonify({
            "response": response,
            "audio_base64": audio_base64
        })

    finally:
        # Cleanup temporary files to ensure no persistent storage
        if os.path.exists(temp_audio_filename):
            os.remove(temp_audio_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
