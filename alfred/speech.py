from google.cloud import speech

from alfred.auth import credentials

# gcs_uri = "gs://maro_bucket/Juan1.wav"


class Speech:
    def __init__(self):
        self.client = speech.SpeechClient(credentials=credentials)

    def transcribe_from_uri(self, gcs_uri):
        audio = speech.RecognitionAudio(uri=gcs_uri)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code="es-ES",
            model="phone_call",
            enable_separate_recognition_per_channel=True,
            audio_channel_count=2,
            enable_word_confidence=True,
            use_enhanced=True,
            enable_word_time_offsets=True,
            diarization_config=speech.SpeakerDiarizationConfig(
                enable_speaker_diarization=True,
                min_speaker_count=2,
                max_speaker_count=0,
            ),
        )

        # Detects speech in the audio file
        operation = self.client.long_running_recognize(config=config, audio=audio)

        print("Waiting for operation to complete...")
        response = operation.result(timeout=600)
        print("Transcription complete...")

        result = []

        for r in response.results:
            result.append([r.channel_tag, r.alternatives[0].transcript])

        return result
