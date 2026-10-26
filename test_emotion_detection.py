"""Unit tests for the EmotionDetection package."""

import unittest
from unittest.mock import patch, MagicMock
from EmotionDetection.emotion_detection import emotion_detector


def _mock_response(status_code, json_body=None):
    """Create a mock requests.Response with the given status and body."""
    mock_resp = MagicMock()
    mock_resp.status_code = status_code
    if json_body is not None:
        import json
        mock_resp.text = json.dumps(json_body)
    else:
        mock_resp.text = ""
    return mock_resp


class TestEmotionDetector(unittest.TestCase):
    """Test suite for the emotion_detector function."""

    # ---- Happy-path tests (mocked) ----

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_joy_dominant(self, mock_post):
        """'I am glad this happened' should return joy as dominant."""
        mock_post.return_value = _mock_response(200, {
            "emotionPredictions": [{"emotion": {
                "anger": 0.01, "disgust": 0.01,
                "fear": 0.01, "joy": 0.95, "sadness": 0.02
            }}]
        })
        result = emotion_detector("I am glad this happened")
        self.assertEqual(result['dominant_emotion'], 'joy')

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_anger_dominant(self, mock_post):
        """'I am really mad about this' should return anger as dominant."""
        mock_post.return_value = _mock_response(200, {
            "emotionPredictions": [{"emotion": {
                "anger": 0.95, "disgust": 0.02,
                "fear": 0.01, "joy": 0.01, "sadness": 0.01
            }}]
        })
        result = emotion_detector("I am really mad about this")
        self.assertEqual(result['dominant_emotion'], 'anger')

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_disgust_dominant(self, mock_post):
        """'I feel disgusted just hearing about this' → disgust."""
        mock_post.return_value = _mock_response(200, {
            "emotionPredictions": [{"emotion": {
                "anger": 0.02, "disgust": 0.93,
                "fear": 0.01, "joy": 0.01, "sadness": 0.03
            }}]
        })
        result = emotion_detector("I feel disgusted just hearing about this")
        self.assertEqual(result['dominant_emotion'], 'disgust')

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_sadness_dominant(self, mock_post):
        """'I am so sad about this' → sadness."""
        mock_post.return_value = _mock_response(200, {
            "emotionPredictions": [{"emotion": {
                "anger": 0.01, "disgust": 0.02,
                "fear": 0.03, "joy": 0.01, "sadness": 0.93
            }}]
        })
        result = emotion_detector("I am so sad about this")
        self.assertEqual(result['dominant_emotion'], 'sadness')

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_fear_dominant(self, mock_post):
        """'I am really afraid that this will happen' → fear."""
        mock_post.return_value = _mock_response(200, {
            "emotionPredictions": [{"emotion": {
                "anger": 0.01, "disgust": 0.01,
                "fear": 0.94, "joy": 0.02, "sadness": 0.02
            }}]
        })
        result = emotion_detector("I am really afraid that this will happen")
        self.assertEqual(result['dominant_emotion'], 'fear')

    # ---- Output structure tests ----

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_output_has_all_keys(self, mock_post):
        """Result dictionary must have all six expected keys."""
        mock_post.return_value = _mock_response(200, {
            "emotionPredictions": [{"emotion": {
                "anger": 0.1, "disgust": 0.1,
                "fear": 0.1, "joy": 0.6, "sadness": 0.1
            }}]
        })
        result = emotion_detector("test text")
        expected_keys = {'anger', 'disgust', 'fear', 'joy',
                         'sadness', 'dominant_emotion'}
        self.assertEqual(set(result.keys()), expected_keys)

    # ---- Error-handling tests ----

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_status_400_returns_none(self, mock_post):
        """HTTP 400 must return all None values."""
        mock_post.return_value = _mock_response(400)
        result = emotion_detector("bad input")
        self.assertIsNone(result['dominant_emotion'])
        for key in ('anger', 'disgust', 'fear', 'joy', 'sadness'):
            self.assertIsNone(result[key])

    def test_blank_input_returns_none(self):
        """Blank / whitespace-only input must return all None values."""
        for blank in ("", "   ", None):
            result = emotion_detector(blank)
            self.assertIsNone(result['dominant_emotion'])
            for key in ('anger', 'disgust', 'fear', 'joy', 'sadness'):
                self.assertIsNone(result[key])


if __name__ == '__main__':
    unittest.main()
