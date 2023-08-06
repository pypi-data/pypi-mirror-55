import logging
from .Base import BaseTranscriber
from google.cloud import speech_v1, speech_v1p1beta1

logging.basicConfig(level=logging.DEBUG,
                    filename='app.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


class TranscriberBeta(BaseTranscriber):

    def __init__(self,
                 output_directory: str,
                 contexts_path: str,
                 credential_path: str,
                 speaker_count: int = 1,
                 diarization: bool = False):

        super().__init__(output_directory=output_directory,
                         contexts_path=contexts_path,
                         credential_path=credential_path)
        self._speech = speech_v1p1beta1
        self._client = self._speech.SpeechClient(credentials=self._credentials)
        self._encoding = self._speech.enums.RecognitionConfig.AudioEncoding.LINEAR16
        self._config = self._speech.types.RecognitionConfig(encoding=self._encoding,
                                                            language_code='en-US',
                                                            enable_word_time_offsets=True,
                                                            max_alternatives=5,
                                                            model='video',
                                                            use_enhanced=True,
                                                            diarization_speaker_count=speaker_count,
                                                            enable_speaker_diarization=diarization)


class TranscriberV1(BaseTranscriber):

    def __init__(self,
                 output_directory: str,
                 contexts_path: str,
                 credential_path: str):

        super().__init__(output_directory=output_directory,
                         contexts_path=contexts_path,
                         credential_path=credential_path)
        self._speech = speech_v1
        self._client = self._speech.SpeechClient(credentials=self._credentials)
        self._encoding = self._speech.enums.RecognitionConfig.AudioEncoding.LINEAR16
        self._config = self._speech.types.RecognitionConfig(encoding=self._encoding,
                                                            language_code='en-US',
                                                            enable_word_time_offsets=True,
                                                            max_alternatives=5,
                                                            model='video',
                                                            use_enhanced=True)




