import os
from typing import List

from fastapi import UploadFile


async def store(directory: str, files: List[UploadFile]):
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    for file in files:
        with open(os.path.join(directory, file.filename), 'wb') as document:
            data = await file.read()
            document.write(data)
