"""
AI Client for Gemini API integration
"""

import os
import google.generativeai as genai
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AIClient:
    """Client for interacting with Google's Gemini AI API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI client"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        
        # Configure the API
        genai.configure(api_key=self.api_key)
        
        # Default model
        self.default_model = "gemini-2.0-flash-exp"
        self.model = None
        
        logger.info("AI Client initialized successfully")
    
    def get_model(self, model_name: Optional[str] = None) -> genai.GenerativeModel:
        """Get a generative model instance"""
        model_name = model_name or self.default_model
        return genai.GenerativeModel(model_name)
    
    def generate_content(self, 
                        prompt: str, 
                        model_name: Optional[str] = None,
                        **kwargs) -> str:
        """
        Generate content using the specified model
        
        Args:
            prompt: The input prompt
            model_name: Model to use (defaults to default_model)
            **kwargs: Additional parameters for generation
            
        Returns:
            Generated text response
        """
        try:
            model = self.get_model(model_name)
            response = model.generate_content(prompt, **kwargs)
            return response.text
        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise
    
    def generate_structured_response(self, 
                                   prompt: str,
                                   output_format: str = "json",
                                   model_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate structured response in specified format
        
        Args:
            prompt: The input prompt
            output_format: Desired output format (json, markdown, etc.)
            model_name: Model to use
            
        Returns:
            Structured response
        """
        # Add format instruction to prompt
        if output_format.lower() == "json":
            formatted_prompt = f"{prompt}\n\nIMPORTANT: Your response MUST be valid JSON. Do not include any text outside the JSON structure. Ensure all strings are properly quoted with double quotes, avoid trailing commas, and escape special characters correctly."
        else:
            formatted_prompt = f"{prompt}\n\nPlease respond in {output_format} format."
        
        response_text = self.generate_content(formatted_prompt, model_name)
        
        # Parse response based on format
        if output_format.lower() == "json":
            import json
            import re
            try:
                # Try to extract JSON if it's embedded in text
                json_match = re.search(r'```json\s*(.+?)\s*```', response_text, re.DOTALL)
                if json_match:
                    json_str = json_match.group(1)
                    return json.loads(json_str)
                
                # Try direct parsing
                return json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.warning(f"Failed to parse JSON response: {e}")
                # Return a properly structured fallback response
                return {
                    "response": {
                        "summary": "Response could not be structured as JSON",
                        "action_items": [{
                            "step": 1,
                            "action": "Review the raw response below",
                            "time_required": "N/A",
                            "cost": "N/A"
                        }],
                        "tips": ["The AI generated an invalid JSON response"],
                        "raw_response": response_text
                    }
                }
        
        return {"response": response_text, "format": output_format}
    
    def chat(self, 
             messages: list,
             model_name: Optional[str] = None) -> str:
        """
        Chat with the model using conversation history
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            model_name: Model to use
            
        Returns:
            Model response
        """
        try:
            model = self.get_model(model_name)
            chat = model.start_chat(history=[])
            
            # Send all messages
            for message in messages:
                if message['role'] == 'user':
                    response = chat.send_message(message['content'])
            
            return response.text
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            raise

