"""
Utility functions
"""

import os
import tempfile
import shutil
from pathlib import Path


def save_uploaded_file(uploaded_file, directory: str = "temp") -> str:
    """
    Save uploaded file to temporary directory
    
    Args:
        uploaded_file: Streamlit uploaded file
        directory: Directory to save to
        
    Returns:
        Path to saved file
    """
    os.makedirs(directory, exist_ok=True)
    
    file_path = os.path.join(directory, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path


def cleanup_temp_files(directory: str = "temp"):
    """
    Clean up temporary files
    
    Args:
        directory: Directory to clean
    """
    if os.path.exists(directory):
        try:
            shutil.rmtree(directory)
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")


def ensure_directory(path: str):
    """Ensure directory exists"""
    Path(path).mkdir(parents=True, exist_ok=True)

