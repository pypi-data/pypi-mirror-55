from google.protobuf.json_format import MessageToJson
from google.oauth2 import service_account
import logging
import os
import json
import textgrid
import pandas as pd
import numpy as np
__author__ = 'Michael Joseph Fox'
__doc_ = 'Collection of base classes for interacting with Google Cloud'

logging.basicConfig(level=logging.DEBUG,
                    filename='transcriber.log',
                    filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


class BaseProxy(object):

    def __init__(self, credential_path: str):
        self._credential_path = credential_path
        self._credentials = service_account.Credentials.from_service_account_file(self._credential_path)


class BaseTranscriber(BaseProxy):

    def __init__(self,
                 output_directory: str,
                 contexts_path: str,
                 credential_path: str):
        """
        Handles transcription and format export of Google Speech-to-Text API
        :param output_directory: Local file folder to store transcriptions
        :param contexts_path: Local path to context file
        :param credential_path: Local path to API credentials
        """
        super().__init__(credential_path=credential_path)
        self._output_directory = output_directory
        self._contexts_path = contexts_path

        self._client = None
        self._speech = None
        self._config = None
        self._transcripts = dict()

        with open(contexts_path, 'r') as data:
            self._contexts = data.readlines()

        if not os.path.exists(self._output_directory):
            os.mkdir(self._output_directory)
            os.mkdir(os.path.join(self._output_directory, 'JSON'))
            os.mkdir(os.path.join(self._output_directory, 'TextGrid'))

    @staticmethod
    def _construct_utterance_intervals(group: pd.DataFrame):
        dt = {'speakerTag': group.loc[:, 'speakerTag'].unique().tolist()[0],
              'word': group.loc[:, 'word'].str.cat(sep=' '),
              'startTime': group.loc[:, 'startTime'].min(),
              'endTime': group.loc[:, 'endTime'].max()}
        return pd.DataFrame(dt, index=[0])

    def read_transcriptions(self, file_paths: list):
        """
        Read in multiple transcription files in JSON format.
        :param file_paths: List of full file paths on disk.
        :type file_paths: list
        :return: self
        """
        for file_path in file_paths:
            self.read_transcription(file_path=file_path)
        return self

    def read_transcription(self, file_path: str):
        """
        Read in a single transcription fine in JSON format.
        :param file_path: Full file path on disk.
        :type file_path: str
        :return: self
        """
        transcription_name = os.path.split(file_path)[-1]
        with open(file_path, 'r', encoding='utf-8') as data:
            transcription = json.load(data)
        self._transcripts.update({transcription_name: transcription})

        return self

    def get_transcriptions(self, uris: list):
        """
        Get transcriptions for multiple audio files.
        :param uris: List of URIs of the form  gs://<bucket name>/<file name>
        :type uris: list
        :return: self
        """
        for uri in uris:
            self.get_transcription(gcs_uri=uri)
        return self

    def get_transcription(self, gcs_uri: str):
        """
        Asynchronously transcribes the audio file specified by the gcs_uri.
        :param gcs_uri: URI of the form gs://<bucket name>/<file name>
        :type gcs_uri: str
        :return: self
        """
        file_name = os.path.split(gcs_uri)[-1]
        out_file_path = os.path.join(self._output_directory, file_name.split('.')[0]+'.json')

        if not os.path.exists(out_file_path):
            self._speech.types.SpeechContext(phrases=self._contexts)
            audio = self._speech.types.RecognitionAudio(uri=gcs_uri)

            try:
                operation = self._client.long_running_recognize(self._config, audio)
                print('Waiting for operation to complete...')

                response = operation.result()
                serialized = MessageToJson(response)
                resp_obj = json.loads(serialized)

                self._transcripts.update({file_name: resp_obj})

                # Each result is for a consecutive portion of the audio. Iterate through
                # them to get the transcripts for the entire audio file.
                with open(os.path.join(self._output_directory,
                                       'JSON',
                                       file_name.split('.')[0] + '.json'),
                          'w') as outfile:

                    json.dump(resp_obj,
                              outfile)

            except Exception as e:
                logging.error('Exception occurred on file: {}, error: {}'.format(file_name, e), exc_info=True)
                pass
        else:
            print('{} exists. Skipping to not overwrite.'.format(out_file_path))
        return self

    def export_textgrids(self):
        """
        Export all transcripts contained in the object instance to Praat TextGrids.
        :return: self
        """
        for k, v in self._transcripts.items():
            self.export_textgrid(file_name=k)
        return self

    def export_textgrid(self, file_name: str):
        """
        Export a Google-Speech API transcription to a Praat TextGrids
        With each utterance as a Interval on a "transcription" tier.
        :param file_name: Full file path to location of transcript.
        :param n_alternatives: Number of alternatives to create tier's for
        :return: self
        """
        # TODO modularize this code more
        transcript = self._transcripts.get(file_name, {}).get('results', [])

        diarinaized_words = transcript[-1].get('alternatives', [])[0].get('words', [])

        speakers_df = pd.DataFrame(diarinaized_words)
        speakers_df.loc[:, 'startTime'] = speakers_df.loc[:, 'startTime'].str.replace('s', '').astype(float)
        speakers_df.loc[:, 'endTime'] = speakers_df.loc[:, 'endTime'].str.replace('s', '').astype(float)
        speakers_df.loc[:, 'segment_type'] = 'W'

        # DETECT PAUSES
        speakers_df.loc[:, 'minShift'] = speakers_df.loc[:, 'startTime'].shift(-1)
        speakers_df.loc[:, 'pauseDetect'] = np.abs(speakers_df.loc[:, 'endTime'] - speakers_df.loc[:, 'minShift'])
        pauses_df = speakers_df.loc[speakers_df.loc[:, 'pauseDetect'] > 0.01, :].copy()

        pauses_df.drop(columns='startTime',
                       inplace=True)
        pauses_df.rename(columns={'minShift': 'endTime',
                                  'endTime': 'startTime'},
                         inplace=True)
        pauses_df.loc[:, 'word'] = 'sp'
        pauses_df.loc[:, 'segment_type'] = 'X'

        speakers_df = pd.concat([speakers_df, pauses_df], sort=True)
        speakers_df.sort_values(by='endTime',
                                inplace=True)
        speakers_df.reset_index(inplace=True,
                                drop=True)

        # Code Utterances
        speakers_df.loc[:, 'utterance_group'] = 0
        pause_idx = speakers_df.loc[speakers_df.loc[:, 'segment_type'] == 'X', :].index.tolist()
        pause_idx.append(max(speakers_df.index.tolist())+1)
        start_slice = 0
        for index, end_slice in enumerate(pause_idx):
            speakers_df.loc[start_slice:end_slice - 1, 'utterance_group'] = index + 1
            start_slice = end_slice + 1

        # Construct utterance intervals
        speakers_df = speakers_df.loc[speakers_df.loc[:, 'utterance_group'] != 0, :]
        utterance_df = speakers_df.groupby(by='utterance_group').apply(self._construct_utterance_intervals)
        n_speakers = speakers_df.loc[:, 'speakerTag'].max()
        max_time = speakers_df.loc[:, 'endTime'].max()

        grid_name = file_name.split('.')[0] + '.TextGrid'
        tg = textgrid.TextGrid(name=file_name,
                               minTime=0,
                               maxTime=max_time)

        # Create speaker tiers
        for i in range(1, n_speakers+1):
            spk_tier = textgrid.IntervalTier(name=i,
                                             minTime=0,
                                             maxTime=max_time)
            # Add word intervals
            n_df = utterance_df.loc[utterance_df.loc[:, 'speakerTag'] == i, :]
            for _, row in n_df.iterrows():
                try:
                    interval = textgrid.Interval(minTime=row['startTime'],
                                                 maxTime=row['endTime'],
                                                 mark=row['word'])
                except ValueError as e:
                    logging.debug(msg='{} contained an interval of length <= 0. '
                                      'Interval time = {}'.format(file_name, e))
                    interval = textgrid.Interval(minTime=row['startTime'],
                                                 maxTime=row['endTime'] + 0.001,
                                                 mark=row['word'])
                    pass

                spk_tier.addInterval(interval=interval)
            tg.append(tier=spk_tier)

        tg.write(f=os.path.join(self._output_directory,
                                'TextGrid',
                                grid_name))

        return self

