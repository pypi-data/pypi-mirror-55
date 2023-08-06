import os
import json
import pickle
import pandas as pd
from unittest import TestCase
from unittest.mock import patch
from Transcriber.Google.Transcriber import TranscriberBeta, TranscriberV1

DIR_NAME = os.path.dirname(__file__)
CONTEXT_PATH = os.path.join(DIR_NAME, 'Data/interview_context.txt')
CREDENTIAL_PATH = os.path.join(DIR_NAME, 'FakeCredentials.json')
OUTPUT_DIRECTORY = os.path.join(DIR_NAME, 'Output')
TEST_DATA_PATH = os.path.join(DIR_NAME, 'Data')

TEST_FILE_NAME = 'TestWav'
TEST_INTERVIEW = TEST_FILE_NAME + '.json'
TEST_TEXTGRID = TEST_FILE_NAME + '.TextGrid'
TEST_UTTERANCES_DF = TEST_FILE_NAME + '_utterances.csv'
TEST_SPEAKERS_DF = TEST_FILE_NAME + '_speakers.csv'


class TestTranscriberBeTa(TestCase):

    def setUp(self) -> None:
        self.transcriber = TranscriberBeta(contexts_path=CONTEXT_PATH,
                                           credential_path=CREDENTIAL_PATH,
                                           output_directory=OUTPUT_DIRECTORY,
                                           speaker_count=2,
                                           diarization=True)
        file_name = os.path.join(TEST_DATA_PATH, TEST_INTERVIEW)
        with open(file_name, 'r') as file:
            resp_obj = json.load(file)
        self.transcriber._transcripts.update({TEST_INTERVIEW: resp_obj})

        with open(os.path.join(TEST_DATA_PATH, TEST_TEXTGRID), 'r') as data:
            self.target_textgrid = data.readlines()

        self.target_dataframe = pd.read_csv(os.path.join(TEST_DATA_PATH, TEST_UTTERANCES_DF))

    def test__construct_utterance_intervals(self):
        test_df = pd.read_csv(os.path.join(TEST_DATA_PATH, TEST_SPEAKERS_DF))
        utterance_df = test_df.groupby(by='utterance_group').apply(self.transcriber._construct_utterance_intervals)
        utterance_df.reset_index(inplace=True,
                                 drop=True)
        self.assertDictEqual(utterance_df.to_dict(),
                             self.target_dataframe.to_dict(),
                             'Constructing utterance dataframe failed.')

    def test_read_transcription(self):
        mock_transcription_path = os.path.join(TEST_DATA_PATH, TEST_INTERVIEW)
        self.transcriber.read_transcription(mock_transcription_path)
        self.assertIsNotNone(self.transcriber._transcripts,
                             msg='Reading in transcript failed entirely.')

    @patch('Transcriber.Google.Transcriber.speech_v1p1beta1.SpeechClient.long_running_recognize')
    def test_get_transcription(self, mock_speech_v1b1beta1):

        class MockLongRunning(object):

            @staticmethod
            def result():
                with open(os.path.join(TEST_DATA_PATH, 'WholeResponse.pkl'), 'rb') as pkl:
                    return pickle.load(pkl)

        mock_speech_v1b1beta1.return_value = MockLongRunning()

        self.transcriber.get_transcription(gcs_uri='MockAPI_Test')
        self.assertTrue(os.path.exists(os.path.join(self.transcriber._output_directory,
                                                    'JSON',
                                                    'MockAPI_Test.json')),
                        msg='API Response was not written to disk.')
        self.assertIsNotNone(self.transcriber._transcripts,
                             msg='API Response was not added to the object.')

    def test_export_textgrid(self):
        self.transcriber.export_textgrid(file_name=TEST_INTERVIEW)
        output_textgrid = os.path.join(OUTPUT_DIRECTORY, 'TextGrid', TEST_TEXTGRID)
        with open(output_textgrid, 'r') as data:
            tg = data.readlines()
        self.assertEquals(tg,
                          self.target_textgrid,
                          'Exporting TextGrid produced a malformed output.')
        os.remove(output_textgrid)


