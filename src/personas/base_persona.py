"""
Base Persona class for Vantage AI PersonaPilot
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
import os

class BasePersona(ABC):
    """Abstract base class for all personas"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.personality_traits = []
        self.expertise_areas = []
        self.communication_style = ""
        self.output_preferences = {}
        self.context_memory = []
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this persona"""
        pass
    
    @abstractmethod
    def get_example_queries(self) -> List[str]:
        """Get example queries this persona can handle"""
        pass
    
    @abstractmethod
    def get_output_format(self) -> Dict[str, Any]:
        """Get preferred output format for this persona"""
        pass
    
    def add_context(self, context: str):
        """Add context to persona's memory"""
        self.context_memory.append(context)
        # Keep only last 10 contexts
        if len(self.context_memory) > 10:
            self.context_memory = self.context_memory[-10:]
    
    def get_context_summary(self) -> str:
        """Get summary of recent context"""
        if not self.context_memory:
            return ""
        return f"Recent context: {'; '.join(self.context_memory[-3:])}"
    
    def format_prompt(self, query: str, context: Optional[str] = None) -> str:
        """Format a complete prompt for this persona"""
        system_prompt = self.get_system_prompt()
        
        # Add context if provided
        context_part = ""
        if context:
            context_part = f"\n\nContext: {context}"
        elif self.context_memory:
            context_part = f"\n\n{self.get_context_summary()}"
        
        # Add output format instructions with clear JSON formatting guidelines
        output_format = self.get_output_format()
        format_instructions = f"""
\nPlease provide your response in valid JSON format exactly matching this structure: 
```json
{json.dumps(output_format, indent=2)}
```

IMPORTANT: Your response MUST be valid JSON. Ensure all strings are properly quoted with double quotes, avoid trailing commas, and escape special characters correctly. Do not include any text outside the JSON structure."""
        
        return f"{system_prompt}{context_part}\n\nUser Query: {query}{format_instructions}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert persona to dictionary"""
        return {
            "name": self.name,
            "description": self.description,
            "personality_traits": self.personality_traits,
            "expertise_areas": self.expertise_areas,
            "communication_style": self.communication_style,
            "output_preferences": self.output_preferences
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BasePersona':
        """Create persona from dictionary"""
        persona = cls(data["name"], data["description"])
        persona.personality_traits = data.get("personality_traits", [])
        persona.expertise_areas = data.get("expertise_areas", [])
        persona.communication_style = data.get("communication_style", "")
        persona.output_preferences = data.get("output_preferences", {})
        return persona

