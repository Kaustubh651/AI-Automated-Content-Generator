"""
Pure utility functions for common operations.
"""

import json
from typing import Any, Dict, List, Optional


def load_json(filepath: str) -> Dict[str, Any]:
    """Load JSON from file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], filepath: str) -> None:
    """Save JSON to file."""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)


def sanitize_text(text: str) -> str:
    """Remove unwanted characters and normalize text."""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove common artifacts
    text = text.replace('[INST]', '').replace('[/INST]', '')
    return text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = ' '.join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks
