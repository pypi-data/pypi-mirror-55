# TranscribeInterviews
Python interface for interacting with the Google Speech-to-Text API and Google Cloud Storage API for the purposes of automatic audio transcription. Usage requires a google cloud account with a credential's file issued from it with permissions for both APIs.

## Installation
```bash
pip install InterviewTranscriber
```

## Example End-to-End Workflow
```python
# 1) Upload audio file(s) to Google Coud Coldline Storage bucket.
from Transcriber.Google.Storage import Storage
from Transcriber.Google.Transcriber import TranscriberBeta

storage_connection = Storage(project_id='<project_id>',
                             credential_path='<path_to_credential_file')
storage_connection.upload_file(bucket_name='<cloud_bucket_name>',
                               source_file_path='<path_to_source_file>')

# 2) Get URI list of files in bucket
file_list = storage_connection.get_uris(bucket_name='<cloud_bucket_name>')

# 3) Send API call to transcribe audio
transcriber = TranscriberBeta(output_directory='<path_to_output_directory>',
                              credential_path='<path_to_credential_file>',
                              contexts_path='<path_to_contexts_file.txt>',
                              speaker_count=2,
                              diarization=True)
        
transcriber.get_transcriptions(uris=file_list) 

# 4) Export as a Praat TextGrid
transcriber.export_textgrids()                    
```

