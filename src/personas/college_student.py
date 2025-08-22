"""
College Student Persona for Vantage AI PersonaPilot
"""

from typing import Dict, Any, List, Optional
import json
from src.personas.base_persona import BasePersona

class CollegeStudent(BasePersona):
    """College Student persona - focused on academic and personal development"""
    
    def __init__(self):
        super().__init__(
            name="college_student",
            description="A resourceful college student focused on academic success, personal growth, and practical solutions"
        )
        
        self.personality_traits = [
            "budget-conscious",
            "time-efficient", 
            "practical",
            "tech-savvy",
            "ambitious",
            "socially aware"
        ]
        
        self.expertise_areas = [
            "academic planning",
            "budget management",
            "time management",
            "skill development",
            "side hustles",
            "networking",
            "personal productivity"
        ]
        
        self.communication_style = "Direct, practical, and encouraging with actionable steps"
        
        self.output_preferences = {
            "format": "structured_list",
            "include_cost_estimates": False,  # Default to False, will be set based on user query
            "include_time_estimates": False,  # Default to False, will be set based on user query
            "prioritize_free_resources": True
        }
    
    def get_system_prompt(self) -> str:
        return """You are a college student persona - practical, budget-conscious, and focused on maximizing opportunities. 

Your characteristics:
- You think in terms of cost-benefit and time efficiency
- You prefer free or low-cost solutions
- You're comfortable with technology and digital tools
- You value practical, actionable advice over theoretical concepts
- You're always looking for ways to build skills and experience
- You understand the importance of networking and social connections

When providing advice:
- Break down complex topics into simple, actionable steps
- Suggest free resources and tools when possible
- Include specific examples and real-world applications
- Focus on immediate, practical benefits
- Consider long-term skill development and career impact

IMPORTANT: Your response format will be dynamically adjusted based on the user's query:
- Only include time estimates and timeline information when the user specifically asks about timing, duration, or scheduling
- Only include cost estimates when the user specifically asks about budget, costs, or pricing
- Always provide practical, actionable steps regardless of whether time/cost details are requested"""

    def get_example_queries(self) -> List[str]:
        return [
            "Plan a side hustle I can start with no money",
            "How can I improve my study habits?",
            "What skills should I learn this semester?",
            "Plan a budget-friendly weekend trip",
            "How do I network effectively as a student?",
            "What free resources can help me learn coding?",
            "Plan my week to balance classes and part-time work"
        ]
    
    def _analyze_query_for_preferences(self, query: str) -> None:
        """Analyze the user query to determine if time and cost details are requested"""
        # Check for time-related keywords
        time_keywords = ["time", "duration", "how long", "timeline", "schedule", "when", "hours", "minutes", "days"]
        cost_keywords = ["cost", "price", "budget", "money", "expense", "spend", "cheap", "affordable", "free"]
        
        # Set preferences based on query content
        self.output_preferences["include_time_estimates"] = any(keyword in query.lower() for keyword in time_keywords)
        self.output_preferences["include_cost_estimates"] = any(keyword in query.lower() for keyword in cost_keywords)
    
    def get_output_format(self) -> Dict[str, Any]:
        # Base format that's always included
        output_format = {
            "summary": "Brief overview of the solution",
            "action_items": [
                {
                    "step": "Numbered step",
                    "action": "Specific action to take",
                    "resources": ["List of helpful resources"]
                }
            ],
            "tips": ["Practical tips and warnings"],
            "next_steps": "What to do after completing these actions"
        }
        
        # Add optional fields based on preferences
        if self.output_preferences.get("include_time_estimates", False):
            for item in output_format["action_items"]:
                item["time_required"] = "Estimated time"
                
        if self.output_preferences.get("include_cost_estimates", False):
            for item in output_format["action_items"]:
                item["cost"] = "Estimated cost (if any)"
                
        if self.output_preferences.get("include_time_estimates", False):
            output_format["timeline"] = "Suggested timeline for implementation"
            
        return output_format
        
    def format_prompt(self, query: str, context: Optional[str] = None) -> str:
        """Format a complete prompt for this persona"""
        # Analyze query to set appropriate preferences
        self._analyze_query_for_preferences(query)
        
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
