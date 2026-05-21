import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("API_KEY"),
    api_secret=os.getenv("API_SECRET")
)

def upload_file(file):

    uploaded_file = cloudinary.uploader.upload(
        file,
        resource_type="auto"
    )

    return uploaded_file["secure_url"]