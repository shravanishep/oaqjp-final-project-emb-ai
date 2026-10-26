# Emotion Detector – Watson NLP Final Project

An AI-powered emotion detection web application built with **Python**, **Flask**, and the **Watson NLP EmotionPredict** service. This is the final project for the Coursera course *"Developing AI Applications with Python and Flask"* (IBM Full-Stack Software Developer Professional Certificate).

## Architecture

```
emotion-detector/
├── EmotionDetection/
│   ├── __init__.py              # Package init – exports emotion_detector
│   └── emotion_detection.py     # Core Watson NLP integration
├── static/
│   └── mywebscript.js           # Frontend AJAX script
├── templates/
│   └── index.html               # Web interface template
├── submission-evidence/         # Coursera grading evidence
├── server.py                    # Flask web application
├── test_emotion_detection.py    # Unit tests (unittest + mock)
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Detected Emotions

The application detects five emotions from input text:

| Emotion   | Description                        |
|-----------|------------------------------------|
| **anger** | Intensity of anger in the text     |
| **disgust** | Intensity of disgust             |
| **fear**  | Intensity of fear                  |
| **joy**   | Intensity of joy                   |
| **sadness** | Intensity of sadness             |

The **dominant emotion** is the one with the highest score.

## Watson NLP Integration

The `emotion_detector()` function sends text to the IBM Watson NLP EmotionPredict endpoint:

```
POST https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict
```

- **Header**: `grpc-metadata-mm-model-id: emotion_aggregated-workflow_lang_en_stock`
- **Body**: `{"raw_document": {"text": "<input>"}}`

> **Note**: This endpoint is only accessible from within the IBM Skills Network lab environment. Running locally outside the lab will result in the function returning `None` values due to connection timeout (handled gracefully).

### Example Output (Illustrative)

```python
{
    'anger': 0.006,
    'disgust': 0.002,
    'fear': 0.009,
    'joy': 0.971,
    'sadness': 0.012,
    'dominant_emotion': 'joy'
}
```

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/emotion-detector.git
cd emotion-detector

# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
python server.py
```

Open your browser at **http://localhost:5000**.

## Running Unit Tests

```bash
python -m unittest test_emotion_detection -v
```

## Running Static Code Analysis

```bash
python -m pylint server.py
python -m pylint EmotionDetection/emotion_detection.py
```

Both files achieve a perfect **10.00/10** Pylint score.

## Error Handling

### HTTP 400 Response
When the Watson NLP API returns status code 400 (e.g., unprocessable input), the function returns a dictionary with all `None` values instead of crashing.

### Blank / Empty Input
Blank or whitespace-only input is caught **before** making any API call. The Flask server returns `"Invalid text! Please try again!"` to the user.

### Connection Errors
If the Watson NLP endpoint is unreachable (e.g., running outside IBM Skills Network), the function catches the `RequestException` and returns `None` values gracefully.

## Submission Evidence

All evidence files for Coursera grading are stored in `submission-evidence/`. See the checklist inside that folder for details.

## License

This project is part of the IBM Full-Stack Software Developer Professional Certificate on Coursera.
