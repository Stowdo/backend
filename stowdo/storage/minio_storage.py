from django.conf import settings
from django.core.files import storage
from django.http import response
from minio import Minio
from io import BytesIO
from re import match


class MinioStorage(storage.Storage):
    def __init__(self, option=None):
        if not option:
            option = settings.MINIO_CONFIG
        self.option = option
        self.client = Minio(
            option.get('host', 'localhost:9000'),
            access_key=option.get('access_key', ''),
            secret_key=option.get('secret_key', ''),
            secure=False)

    @staticmethod
    def create_valid_bucket_name(name):
        regex_char = r'[a-z0-9\\.\\-]'
        result = 'bucket-'

        for index, c in enumerate(name):
            if not match(regex_char, c):
                result += '-'
            else:
                result += c
        
        return result[:61] + '0'

    def create_object_path(self, name):
        reps = name.split('/')

        if not reps:
            raise ValueError('No bucket found in name')
        if len(reps) == 1:
            return self.create_valid_bucket_name(
                self.option.get('default_bucket_name', 'default')
            ), reps[0]
        else:
            return self.create_valid_bucket_name(reps[0]), '.'.join(reps[1:])

    def _open(self, name, mode='rb'):
        bucket, obj = self.create_object_path(name)

        if 'w' in mode:
            raise ValueError(
                'MinioStorage does not handle writing files directly. Use _save instead')
        if not self.client.bucket_exists(bucket):
            raise ValueError('This bucket does not exists')

        output = bytes()
        response = BytesIO()

        try:
            response = self.client.get_object(bucket, obj)
        except Exception as e:
            pass
        else:
            output = BytesIO(response.data)
        finally:
            response.close()

        return output

    def _save(self, name, content):
        bucket, obj = self.create_object_path(name)

        if not self.client.bucket_exists(bucket):
            self.client.make_bucket(bucket)

        self.client.put_object(bucket, obj, content, content.size)
        return name

    def delete(self, name):
        self.client.remove_object(*self.create_object_path(name))

    def exists(self, name):
        bucket, obj = self.create_object_path(name)

        try:
            self.client.stat_object(bucket, obj)
        except Exception:
            return False
        else:
            return True

    def size(self, name):
        bucket, obj = self.create_object_path(name)
        reps = name.split('/')

        try:
            response = self.client.stat_object(bucket, obj)
        except Exception:
            return 0
        else:
            return response.size

    def url(self, name):
        bucket, obj = self.create_object_path(name)
        return bucket + '/' + obj
