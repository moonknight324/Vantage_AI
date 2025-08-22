"""
Output Formatter for Vantage AI PersonaPilot
"""

from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class OutputFormatter:
    """Format and structure AI responses for different personas"""
    
    def __init__(self):
        self.formatters = {
            "json": self._format_json,
            "markdown": self._format_markdown,
            "structured_list": self._format_structured_list,
            "itinerary": self._format_itinerary,
            "technical_guide": self._format_technical_guide,
            "business_plan": self._format_business_plan,
            "story_outline": self._format_story_outline,
            "business_strategy": self._format_business_strategy
        }
    
    def format_response(self, 
                       response_data: Any, 
                       format_type: str = "structured_list",
                       persona_name: str = "default") -> str:
        """
        Format response based on specified format type
        
        Args:
            response_data: Raw response data
            format_type: Desired output format
            persona_name: Name of the persona for context
            
        Returns:
            Formatted response string
        """
        formatter = self.formatters.get(format_type, self._format_default)
        
        try:
            return formatter(response_data, persona_name)
        except Exception as e:
            logger.error(f"Error formatting response: {e}")
            return self._format_default(response_data, persona_name)
    
    def _format_json(self, data: Any, persona_name: str) -> str:
        """Format as JSON"""
        if isinstance(data, str):
            try:
                # Try to parse as JSON first
                parsed = json.loads(data)
                return json.dumps(parsed, indent=2)
            except json.JSONDecodeError:
                return data
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _format_markdown(self, data: Any, persona_name: str) -> str:
        """Format as Markdown"""
        if isinstance(data, dict):
            return self._dict_to_markdown(data)
        elif isinstance(data, str):
            return data
        else:
            return str(data)
    
    def _format_structured_list(self, data: Any, persona_name: str) -> str:
        """Format as structured list with emojis and formatting"""
        if isinstance(data, dict):
            return self._format_dict_as_list(data)
        elif isinstance(data, str):
            return data
        else:
            return str(data)
    
    def _format_itinerary(self, data: Any, persona_name: str) -> str:
        """Format travel itinerary"""
        if not isinstance(data, dict):
            return str(data)
        
        output = []
        
        # Header
        if "destination" in data:
            output.append(f"🗺️ **Destination**: {data['destination']}")
        if "total_budget" in data:
            output.append(f"💰 **Total Budget**: {data['total_budget']}")
        if "duration" in data:
            output.append(f"⏱️ **Duration**: {data['duration']}")
        
        # Itinerary
        if "itinerary" in data:
            output.append("\n📅 **Daily Itinerary**:")
            for day in data["itinerary"]:
                output.append(f"\n**Day {day.get('day', '')}**:")
                
                # Activities
                if "activities" in day:
                    for activity in day["activities"]:
                        time = activity.get("time", "")
                        action = activity.get("activity", "")
                        cost = activity.get("cost", "")
                        location = activity.get("location", "")
                        
                        activity_line = f"  {time}: {action}"
                        if cost:
                            activity_line += f" (💰 {cost})"
                        if location:
                            activity_line += f" @ {location}"
                        output.append(activity_line)
                
                # Accommodation
                if "accommodation" in day:
                    acc = day["accommodation"]
                    output.append(f"  🏨 **Accommodation**: {acc.get('name', '')} (💰 {acc.get('cost', '')})")
                
                # Transportation
                if "transportation" in day:
                    trans = day["transportation"]
                    output.append(f"  🚗 **Transport**: {trans.get('method', '')} (💰 {trans.get('cost', '')})")
        
        # Budget breakdown
        if "budget_breakdown" in data:
            output.append("\n💳 **Budget Breakdown**:")
            for category, amount in data["budget_breakdown"].items():
                output.append(f"  {category.title()}: {amount}")
        
        # Tips
        if "money_saving_tips" in data:
            output.append("\n💡 **Money-Saving Tips**:")
            for tip in data["money_saving_tips"]:
                output.append(f"  • {tip}")
        
        return "\n".join(output)
    
    def _format_technical_guide(self, data: Any, persona_name: str) -> str:
        """Format technical guide"""
        if not isinstance(data, dict):
            return str(data)
        
        output = []
        
        # Problem analysis
        if "problem_analysis" in data:
            output.append(f"🔍 **Problem Analysis**: {data['problem_analysis']}")
        
        # Solution overview
        if "solution_overview" in data:
            output.append(f"💡 **Solution Overview**: {data['solution_overview']}")
        
        # Implementation steps
        if "implementation" in data:
            output.append("\n⚙️ **Implementation Steps**:")
            for step in data["implementation"]:
                output.append(f"\n**Step {step.get('step', '')}**: {step.get('description', '')}")
                
                if "code_example" in step:
                    output.append(f"```\n{step['code_example']}\n```")
                
                if "explanation" in step:
                    output.append(f"*Why*: {step['explanation']}")
                
                if "considerations" in step:
                    output.append("**Considerations**:")
                    for consideration in step["considerations"]:
                        output.append(f"  • {consideration}")
        
        # Code examples
        if "code_examples" in data:
            output.append("\n💻 **Code Examples**:")
            for example in data["code_examples"]:
                output.append(f"\n**{example.get('language', '')}** ({example.get('filename', '')}):")
                output.append(f"```{example.get('language', '')}\n{example.get('code', '')}\n```")
                if "usage" in example:
                    output.append(f"*Usage*: {example['usage']}")
        
        return "\n".join(output)
    
    def _format_business_plan(self, data: Any, persona_name: str) -> str:
        """Format business plan"""
        if not isinstance(data, dict):
            return str(data)
        
        output = []
        
        # Market analysis
        if "market_analysis" in data:
            output.append("📊 **Market Analysis**:")
            for key, value in data["market_analysis"].items():
                output.append(f"  **{key.replace('_', ' ').title()}**: {value}")
        
        # Strategy
        if "strategy" in data:
            output.append("\n🎯 **Strategy**:")
            for key, value in data["strategy"].items():
                output.append(f"  **{key.replace('_', ' ').title()}**: {value}")
        
        # Execution plan
        if "execution_plan" in data:
            output.append("\n📋 **Execution Plan**:")
            for phase in data["execution_plan"]:
                output.append(f"\n**{phase.get('phase', '')}** ({phase.get('timeline', '')}):")
                if "objectives" in phase:
                    output.append("  **Objectives**:")
                    for obj in phase["objectives"]:
                        output.append(f"    • {obj}")
                if "actions" in phase:
                    output.append("  **Actions**:")
                    for action in phase["actions"]:
                        output.append(f"    • {action}")
        
        return "\n".join(output)
    
    def _format_story_outline(self, data: Any, persona_name: str) -> str:
        """Format story outline"""
        if not isinstance(data, dict):
            return str(data)
        
        output = []
        
        # Story concept
        if "story_concept" in data:
            output.append("📖 **Story Concept**:")
            for key, value in data["story_concept"].items():
                if isinstance(value, list):
                    output.append(f"  **{key.replace('_', ' ').title()}**: {', '.join(value)}")
                else:
                    output.append(f"  **{key.replace('_', ' ').title()}**: {value}")
        
        # World building
        if "world_building" in data:
            output.append("\n🌍 **World Building**:")
            for key, value in data["world_building"].items():
                output.append(f"  **{key.replace('_', ' ').title()}**: {value}")
        
        # Characters
        if "characters" in data:
            output.append("\n👥 **Characters**:")
            for char in data["characters"]:
                output.append(f"\n**{char.get('name', '')}** ({char.get('role', '')}):")
                output.append(f"  Background: {char.get('background', '')}")
                output.append(f"  Motivation: {char.get('motivation', '')}")
                output.append(f"  Arc: {char.get('arc', '')}")
        
        return "\n".join(output)
    
    def _format_business_strategy(self, data: Any, persona_name: str) -> str:
        """Format business strategy"""
        if not isinstance(data, dict):
            return str(data)
        
        output = []
        
        # Strategic overview
        if "strategic_overview" in data:
            output.append("🎯 **Strategic Overview**:")
            for key, value in data["strategic_overview"].items():
                output.append(f"  **{key.replace('_', ' ').title()}**: {value}")
        
        # Action plan
        if "action_plan" in data:
            output.append("\n📋 **Action Plan**:")
            for phase in data["action_plan"]:
                output.append(f"\n**{phase.get('phase', '')}** ({phase.get('timeline', '')}):")
                if "objectives" in phase:
                    output.append("  **Objectives**:")
                    for obj in phase["objectives"]:
                        output.append(f"    • {obj}")
                if "actions" in phase:
                    output.append("  **Actions**:")
                    for action in phase["actions"]:
                        output.append(f"    • {action}")
        
        return "\n".join(output)
    
    def _format_dict_as_list(self, data: Dict[str, Any]) -> str:
        """Format dictionary as structured list"""
        output = []
        
        for key, value in data.items():
            if isinstance(value, list):
                output.append(f"**{key.replace('_', ' ').title()}**:")
                for item in value:
                    output.append(f"  • {item}")
            elif isinstance(value, dict):
                output.append(f"**{key.replace('_', ' ').title()}**:")
                for sub_key, sub_value in value.items():
                    output.append(f"  {sub_key.replace('_', ' ').title()}: {sub_value}")
            else:
                output.append(f"**{key.replace('_', ' ').title()}**: {value}")
        
        return "\n".join(output)
    
    def _dict_to_markdown(self, data: Dict[str, Any], level: int = 0) -> str:
        """Convert dictionary to markdown"""
        output = []
        indent = "  " * level
        
        for key, value in data.items():
            # Format key for display
            display_key = key.replace('_', ' ').title()
            
            if isinstance(value, dict):
                output.append(f"{indent}## {display_key}")
                output.append(self._dict_to_markdown(value, level + 1))
            elif isinstance(value, list):
                output.append(f"{indent}### {display_key}")
                for item in value:
                    if isinstance(item, dict):
                        # For dictionaries in lists, format each key-value pair
                        item_output = []
                        for item_key, item_value in item.items():
                            item_display_key = item_key.replace('_', ' ').title()
                            item_output.append(f"**{item_display_key}**: {item_value}")
                        output.append(f"{indent}- {' | '.join(item_output)}")
                    else:
                        output.append(f"{indent}- {item}")
            else:
                output.append(f"{indent}**{display_key}**: {value}")
        
        return "\n".join(output)
    
    def _format_default(self, data: Any, persona_name: str) -> str:
        """Default formatter"""
        if isinstance(data, dict):
            return self._format_dict_as_list(data)
        else:
            return str(data)

