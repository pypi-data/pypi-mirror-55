import os
from .Base import BaseProxy
from google.cloud import storage


class Storage(BaseProxy):

    def __init__(self, credential_path: str, project_id: str):
        super().__init__(credential_path=credential_path)
        self._project_id = project_id
        self._client = storage.Client(project=self._project_id,
                                      credentials=self._credentials)
        self._buckets = []

    def get_all_bucket_names(self):
        self._buckets = list(self._client.list_buckets())
        return self

    def create_bucket(self, bucket_name: str):
        self._client.create_bucket(bucket_or_name=bucket_name,
                                   project=self._project_id)
        self._buckets.append(bucket_name)
        return self

    def upload_file(self, bucket_name: str, source_file_path: str):
        """Upload a file to a bucket"""
        destination_name = os.path.split(source_file_path)[-1]
        bucket = self._client.get_bucket(bucket_name)
        blob = bucket.blob(destination_name)
        blob.upload_from_filename(source_file_path)
        return self

    def delete_file(self, bucket_name, blob_name):
        """Deletes a file from the bucket"""
        bucket = self._client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.delete()
        return self

    def get_blobs(self, bucket_name: str) -> list:
        bucket = self._client.get_bucket(bucket_name)
        blobs = list(bucket.list_blobs())
        return blobs

    def get_uris(self, bucket_name: str) -> list:
        blobs = self.get_blobs(bucket_name=bucket_name)
        uris = ['gs://{}/{}'.format(bucket_name, blob.name) for blob in blobs]
        return uris

