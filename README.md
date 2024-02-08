#Frontend


This Gyaani 🤖 AI Voice Assistant enables users to record audio, process it on a server, and play the processed audio back within the application. It consists of four components:

#React Components

1. Main.js:

- Purpose:
    - Manages the overall application state.
    - Coordinates interactions between other components.
    - Handles server communication for audio processing and playback.
- Key Functions:
    - createBlobUrl: Creates a temporary URL for audio data.
    - handleStop: Processes recorded audio:
        - Fetches the audio data from the Blob URL.
        - Uploads it to the server for processing.
        - Retrieves and plays back the processed audio.
- State Management:
    - btnClkd: (Functionality unclear in the provided code.)
    - isLoading: Indicates whether data is being processed.
    - messages: (Contents and purpose unclear in the provided code.)

2. Reco.js:

- Purpose:
    - Handles audio recording functionality.
    - Interacts with the browser's MediaRecorder API.
- Key Components:
    - ReactMediaRecorder: Provides a wrapper for recording audio.
    - MicButton: Renders a button to initiate audio recording.
- Props:
    - handleStop: Callback function to handle processed audio.

3. Top.js:

- Purpose:
    - Provides a button to reset the conversation.
- Key Functions:
    - resetConversation: Sends a request to the server to reset messages.
- Props:
    - setMessages: Callback function to update the messages state.

4. MicButton.js:

- Purpose:
    - Renders a visually interactive microphone button.
- State Management:
    - isClicked: Tracks whether the button is clicked.
- Handlers:
    - handleClick: Toggles the button's visual state.

Dependencies:

- axios: For making HTTP requests to the server.
- react-media-recorder: For simplifying audio recording.

Server Requirements:

- The server at http://localhost:8000/ should:
    - Accept audio file uploads.
    - Process audio files in a way that's compatible with the client.
    - Return processed audio data in a format that can be played back in the client (details needed).
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Backend

GYAANI is a cutting-edge AI voice assistant specializing in the Indian context. Leveraging advanced machine learning models and leveraging OpenAI and ElevenLabs technologies, GYAANI delivers informative and humorous responses to voice queries while maintaining a high level of cultural relevance.

Functionalities:

- Speech-to-Text Conversion: Accurately transcribes audio input using OpenAI's Whisper model.
- Contextual Response Generation: Employs OpenAI's GPT-3.5-turbo model to deliver comprehensive and relevant responses aligned with the Indian context.
- Text-to-Speech Synthesis: Converts text responses into natural-sounding audio using ElevenLabs Text-to-Speech API.
- Conversation History Management: Efficiently stores and manages conversation history for personalized interactions.

Technical Specifications:

- Server Framework: FastAPI
- API Keys: Secured and managed through .env file for enhanced security.
- Dependencies:
    - fastapi
    - openai
    - elevenlabs
    - requests
    - dotenv

API Endpoints:

- /reset/ (GET): Resets the conversation history by clearing the database.json file.
- / (POST): Receives audio input, processes it through the NLP pipeline, and returns an audio response.

CORS Configuration:

- By default, requests from origins http://localhost:8000/ and http://localhost:8000/reset are permitted. For production environments, configure CORS appropriately to ensure security.

Additional Notes:

- Response length aims to stay under 40 words, prioritizing conciseness.
- Humor is carefully incorporated to enhance user engagement.
- Training data carefully selected to deliver culturally relevant and insightful responses.
- Robust error handling and exception management are planned for future enhancements.


I trust this refined documentation presents GYAANI's capabilities in a more professional and comprehensive manner. Feel free to ask for further clarifications or specific details.
