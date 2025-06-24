from typing import Optional, Dict, Any
from pydantic import BaseModel


class ToolResponse(BaseModel):
    """
    Standardized response format used by all agent tool functions.

    Attributes:
        success (bool): Whether the operation was successful.
        data (Optional[dict]): Function-specific data payload if successful.
        error (Optional[str]): Error message if the operation failed.
    """

    success: bool
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
