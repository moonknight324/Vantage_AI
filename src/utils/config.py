"""
Configuration management for Vantage AI PersonaPilot
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class Config:
    """Configuration management class"""
    
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # API Configuration
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        self.default_model = os.getenv('DEFAULT_MODEL', 'gemini-2.0-flash-exp')
        
        # Application Configuration
        self.debug = os.getenv('DEBUG', 'False').lower() == 'true'
        self.log_level = os.getenv('LOG_LEVEL', 'INFO')
        
        # RAG Configuration
        self.vector_db_path = os.getenv('VECTOR_DB_PATH', 'data/vector_db')
        self.embedding_model = os.getenv('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
        self.max_retrieval_results = int(os.getenv('MAX_RETRIEVAL_RESULTS', '5'))
        
        # Persona Configuration
        self.default_persona = os.getenv('DEFAULT_PERSONA', 'college_student')
        self.max_context_length = int(os.getenv('MAX_CONTEXT_LENGTH', '1000'))
        
        # Output Configuration
        self.default_output_format = os.getenv('DEFAULT_OUTPUT_FORMAT', 'structured')
        self.max_response_length = int(os.getenv('MAX_RESPONSE_LENGTH', '2000'))
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return getattr(self, key, default)
    
    def set(self, key: str, value: Any):
        """Set configuration value"""
        setattr(self, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'gemini_api_key': self.gemini_api_key,
            'default_model': self.default_model,
            'debug': self.debug,
            'log_level': self.log_level,
            'vector_db_path': self.vector_db_path,
            'embedding_model': self.embedding_model,
            'max_retrieval_results': self.max_retrieval_results,
            'default_persona': self.default_persona,
            'max_context_length': self.max_context_length,
            'default_output_format': self.default_output_format,
            'max_response_length': self.max_response_length
        }
    
    def validate(self) -> bool:
        """Validate configuration"""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required")
        return True

