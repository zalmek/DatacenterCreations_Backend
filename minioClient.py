import os

from minio import Minio

from dcapi.models import Components

minio_url = "127.0.0.1:9000"
minio_bucket = "images"
client = Minio(endpoint=minio_url,  # адрес сервера
               access_key='minioadmin',  # логин админа
               secret_key='minioadmin',  # пароль админа
               secure=False)  # опциональный параметр, отвечающий за вкл/выкл защищенное TLS соединение


def add_new_bucket(name):
    client.make_bucket(name)


def load_file(filename):
    client.fput_object(bucket_name=minio_bucket,  # необходимо указать имя бакета,
                       object_name=filename,  # имя для нового файла в хринилище
                       file_path="dcapi/static/%s" % filename)


# for filename in os.listdir("dcapi/static"):
#     load_file(filename)

