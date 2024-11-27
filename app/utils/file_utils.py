import os
import aiofiles
from app.config import BOOKS_DIRECTORY
from fastapi import HTTPException

os.makedirs(BOOKS_DIRECTORY, exist_ok=True)

async def save_file(file, filename: str):
    try:
        print(file,"------------")
        file_path = os.path.join(BOOKS_DIRECTORY, filename)
        print(file_path)
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()  
            await f.write(content)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File path not found: {str(e)}")

    return file_path

def delete_file(file_path: str):
    """
    Deletes a file from the file system.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File not found: {file_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")
