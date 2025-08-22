"""
Persona Manager for Vantage AI PersonaPilot
"""

from typing import Dict, Any, List, Optional
import logging
from .ai_client import AIClient
from src.personas import (
    CollegeStudent, BudgetTraveler, Developer, 
    StartupFounder, SciFiWriter, Businessman
)

logger = logging.getLogger(__name__)

class PersonaManager:
    """Manages persona selection and interactions"""
    
    def __init__(self, ai_client: AIClient):
        self.ai_client = ai_client
        self.personas = {}
        self.active_persona = None
        self._initialize_personas()
    
    def _initialize_personas(self):
        """Initialize all available personas"""
        persona_classes = [
            CollegeStudent,
            BudgetTraveler,
            Developer,
            StartupFounder,
            SciFiWriter,
            Businessman
        ]
        
        for persona_class in persona_classes:
            persona = persona_class()
            self.personas[persona.name] = persona
            logger.info(f"Initialized persona: {persona.name}")
    
    def list_personas(self) -> List[str]:
        """Get list of available persona names"""
        return list(self.personas.keys())
    
    def get_persona(self, persona_name: str):
        """Get a specific persona by name"""
        if persona_name not in self.personas:
            raise ValueError(f"Persona '{persona_name}' not found. Available: {self.list_personas()}")
        return self.personas[persona_name]
    
    def set_active_persona(self, persona_name: str):
        """Set the active persona for the session"""
        self.active_persona = self.get_persona(persona_name)
        logger.info(f"Active persona set to: {persona_name}")
    
    def get_response(self, 
                    persona_name: str, 
                    query: str, 
                    context: Optional[str] = None,
                    output_format: str = "structured") -> str:
        """
        Get a response from a specific persona
        
        This method handles both system prompts (from persona) and user prompts (query)
        
        Args:
            persona_name: Name of the persona to use
            query: User's query (user prompt)
            context: Optional context information
            output_format: Desired output format
            
        Returns:
            Persona's response
        """
        # This method handles both system prompts (from persona) and user prompts (query)
        persona = self.get_persona(persona_name)
        
        # Add context to persona's memory
        if context:
            persona.add_context(context)
        
        # Format the prompt for this persona
        prompt = persona.format_prompt(query, context)
        
        try:
            if output_format == "structured":
                # Get structured response
                response = self.ai_client.generate_structured_response(
                    prompt, 
                    output_format="json"
                )
                return self._format_structured_response(response, persona)
            elif output_format == "raw":
                # Get raw structured response without formatting
                return self.ai_client.generate_structured_response(
                    prompt, 
                    output_format="json"
                )
            else:
                # Get plain text response
                return self.ai_client.generate_content(prompt)
                
        except Exception as e:
            logger.error(f"Error getting response from {persona_name}: {e}")
            return f"Sorry, I encountered an error while processing your request: {str(e)}"
    
    def _format_structured_response(self, response: Dict[str, Any], persona) -> str:
        """Format structured response for better readability"""
        try:
            if "response" in response and isinstance(response["response"], dict):
                data = response["response"]
            else:
                data = response
            
            # Format based on persona's output preferences
            if persona.output_preferences.get("format") == "structured_list":
                return self._format_as_list(data)
            else:
                return self._format_as_text(data)
                
        except Exception as e:
            logger.warning(f"Error formatting structured response: {e}")
            return str(response)
    
    def _format_as_list(self, data: Dict[str, Any]) -> str:
        """Format response as a structured list"""
        output = []
        
        if "summary" in data:
            output.append(f"📋 **Summary**: {data['summary']}")
        
        if "action_items" in data:
            output.append("\n🎯 **Action Items**:")
            for item in data["action_items"]:
                step = f"  {item.get('step', '•')}. {item.get('action', '')}"
                if item.get('time_required'):
                    step += f" (⏱️ {item['time_required']})"
                if item.get('cost'):
                    step += f" (💰 {item['cost']})"
                output.append(step)
                
                if item.get('resources'):
                    resources = ", ".join(item['resources'])
                    output.append(f"    📚 Resources: {resources}")
        
        if "timeline" in data:
            output.append(f"\n📅 **Timeline**: {data['timeline']}")
        
        if "tips" in data:
            output.append("\n💡 **Tips**:")
            for tip in data["tips"]:
                output.append(f"  • {tip}")
        
        if "next_steps" in data:
            output.append(f"\n🚀 **Next Steps**: {data['next_steps']}")
        
        return "\n".join(output)
    
    def _format_as_text(self, data: Dict[str, Any]) -> str:
        """Format response as plain text"""
        if isinstance(data, str):
            return data
        
        # Convert dict to readable text
        output = []
        for key, value in data.items():
            if isinstance(value, list):
                output.append(f"{key.title()}: {', '.join(map(str, value))}")
            else:
                output.append(f"{key.title()}: {value}")
        
        return "\n".join(output)
    
    def get_persona_info(self, persona_name: str) -> Dict[str, Any]:
        """Get detailed information about a persona"""
        persona = self.get_persona(persona_name)
        info = persona.to_dict()
        info["example_queries"] = persona.get_example_queries()
        return info
    
    def create_custom_persona(self, 
                            name: str, 
                            description: str,
                            personality_traits: List[str],
                            expertise_areas: List[str],
                            communication_style: str) -> str:
        """Create a custom persona (placeholder for future implementation)"""
        # This would be implemented to allow users to create custom personas
        logger.info(f"Custom persona creation requested: {name}")
        return f"Custom persona '{name}' creation feature coming soon!"
