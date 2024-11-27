from fastapi import APIRouter, Form, File, UploadFile, Depends, HTTPException,Path
from app.middleware.role_check import require_role
from app.utils.db_utils import books_collection
from typing import Optional
from app.utils.file_utils import save_file, delete_file
from bson import ObjectId
from fastapi.responses import JSONResponse
from app.models.book_model import BookUpdate

router = APIRouter()


@router.post("/books/", dependencies=[Depends(require_role("Admin"))])
async def add_book(
    title: str = Form(...), 
    author: str = Form(...),
    description: str = Form(...),
    available_copies: str = Form(...),
    file: Optional[UploadFile] = File(None)  
):
    if file:
        try:
            file_path = await save_file(file, file.filename)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")
    else:
        file_path = None
        print("No file uploaded")

    book_found = books_collection.find_one({"title": title})
    
    if book_found:
        raise HTTPException(status_code=404, detail="duplicate book found")
    else:
        try:
            book_id = books_collection.insert_one({
                "title": title,
                "author": author,
                "description":description,
                "available_copies":available_copies,
                "file_path": file_path
            }).inserted_id
            return {"message": "Book added", "book_id": str(book_id)}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to add book: {e}")
        
        
        
@router.get("/", dependencies=[Depends(require_role("Admin", "Member"))])
def get_homepage():
    return {"message": "Welcome to Library"}

   
@router.get("/books/", dependencies=[Depends(require_role("Admin", "Member"))])
def get_all_books():
    try:
        # Fetch all books from the collection
        books = books_collection.find()
        
        books_list = []
        for book in books:
            books_list.append({
                "id": str(book["_id"]),  # Convert ObjectId to string
                "title": book["title"],
                "author": book["author"],
                "description": book["description"],
                "available_copies": book["available_copies"],
                "file_path": book.get("file_path", None)  # Handle optional file path
            })

        return {"books": books_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch books: {e}")
    
    

@router.get("/books/{id}", dependencies=[Depends(require_role("Admin", "Member"))])
def get_book(id: str = Path(..., description="The ID of the book to retrieve")):
    try:
        # Fetch the book by ID
        book = books_collection.find_one({"_id": ObjectId(id)})

        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        # Convert the MongoDB document to a dictionary and prepare the response
        book_data = {
            "id": str(book["_id"]),  # Convert ObjectId to string
            "title": book["title"],
            "author": book["author"],
            "description": book["description"],
            "available_copies": book["available_copies"],
            "file_path": book.get("file_path", None)  # Handle optional file path
        }

        return {"book": book_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch book: {e}")
    
    
    
@router.put("/books/{book_id}", dependencies=[Depends(require_role("Admin"))])
def update_book(book_id: str, book_data: BookUpdate):
    """
    Update details of an existing book.
    Admins only.
    """
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")

    result = books_collection.find_one_and_update(
        {"_id": ObjectId(book_id)},
        {"$set": book_data.dict(exclude_unset=True)},
        return_document=True
    )

    if not result:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book updated successfully", "updated_book": book_data.dict(exclude_unset=True)}



@router.delete("/books/{book_id}", dependencies=[Depends(require_role("Admin"))])
def delete_book(book_id: str):
    """
    Delete a book by its ID and remove the associated file.
    Admins only.
    """
    if not ObjectId.is_valid(book_id):
        raise HTTPException(status_code=400, detail="Invalid book ID")

    # Find the book to get the file path
    book = books_collection.find_one({"_id": ObjectId(book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Delete the associated file
    if "file_path" in book and book["file_path"]:
        delete_file(book["file_path"])

    # Delete the book document from the database
    result = books_collection.delete_one({"_id": ObjectId(book_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Failed to delete book")

    return {"message": "Book and associated file deleted successfully"}
