"""Emotion Detection module using Watson NLP EmotionPredict service."""

import json
import requests


def emotion_detector(text_to_analyze):
    """Analyze text and return emotion scores with the dominant emotion.

    Args:
        text_to_analyze (str): The text string to analyze for emotions.

    Returns:
        dict: A dictionary containing scores for anger, disgust, fear,
              joy, sadness, and the dominant_emotion key. Returns None
              values when input is blank or the API returns status 400.
    """
    none_result = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    # Handle blank or empty input before making the API call
    if not text_to_analyze or not text_to_analyze.strip():
        return none_result

    url = (
        'https://sn-watson-emotion.labs.skills.network'
        '/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    header = {
        "grpc-metadata-mm-model-id":
            "emotion_aggregated-workflow_lang_en_stock"
    }
    input_json = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(
            url, json=input_json, headers=header, timeout=10
        )
    except requests.exceptions.RequestException:
        return none_result

    # Handle HTTP 400 – invalid or unprocessable input
    if response.status_code == 400:
        return none_result

    try:
        formatted_response = json.loads(response.text)
        emotions = formatted_response['emotionPredictions'][0]['emotion']
    except (json.JSONDecodeError, KeyError, IndexError):
        return none_result

    anger_score = emotions['anger']
    disgust_score = emotions['disgust']
    fear_score = emotions['fear']
    joy_score = emotions['joy']
    sadness_score = emotions['sadness']

    # Build the result dictionary
    emotion_scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score
    }

    # The dominant emotion is the one with the highest score
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    emotion_scores['dominant_emotion'] = dominant_emotion
    return emotion_scores
