from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
import uvicorn
from typing import Optional

# Import your ISBNReader class
from isbn_reader import ISBNReader # Ensure isbn_reader.py is in the same directory or accessible via PYTHONPATH

class BookInfoResponse(BaseModel):
    """
    API response model for ISBN.
    """
    isbn: Optional[str] = None
    is_valid: Optional[bool] = None # Added for ISBN validation status

app = FastAPI()

@app.post("/recognize-isbn/", response_model=BookInfoResponse)
async def recognize_isbn_endpoint(image_file: UploadFile = File(...)):
    """
    API endpoint to recognize ISBN from an uploaded image.
    """
    recognized_isbn = await ISBNReader.read_from_image(image_file)

    is_isbn_valid = False
    if recognized_isbn: # Only validate if something was recognized
        is_isbn_valid = ISBNReader.validate_isbn(recognized_isbn)

    return BookInfoResponse(isbn=recognized_isbn, is_valid=is_isbn_valid)

if __name__ == "__main__":
    print("Starting FastAPI server for ISBN recognition...")
    print("Access the API documentation at: http://127.0.0.1:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
