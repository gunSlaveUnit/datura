import gzip
import os
from typing import List, BinaryIO

from fastapi import UploadFile


CHUNK_SIZE = 8192
MEDIA_TYPE = "application/gzip"


async def store(directory: str, files: List[UploadFile]):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    for file in files:
        with open(os.path.join(directory, file.filename), 'wb') as document:
            data = await file.read()
            document.write(data)


def _read_chunks(file_object: BinaryIO, chunk_size: int) -> bytes:
    while chunk := file_object.read(chunk_size):
        yield chunk


def read_uncompressed_chunks(file_path: str, chunk_size: int) -> bytes:
    with open(file_path, "rb") as file:
        for chunk in _read_chunks(file, chunk_size):
            yield chunk


def read_compressed_chunks(file_path: str, chunk_size: int) -> bytes:
    with open(file_path, "rb") as file:
        for chunk in _read_chunks(file, chunk_size):
            yield gzip.compress(chunk)
