#!/usr/bin/env python3
"""
Vantage AI PersonaPilot - Main Application Entry Point
"""

import os
import sys
import time
import json
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.persona_manager import PersonaManager
from src.core.ai_client import AIClient
from src.core.output_formatter import OutputFormatter
from src.utils.config import Config
from src.utils.logger import setup_logger

def display_loading_animation(seconds):
    """Display a simple loading animation"""
    animation = ["|    ", "|=   ", "|==  ", "|=== ", "|====", " ====", "  ===", "   ==", "    =", "     "]
    for i in range(seconds * 2):
        sys.stdout.write("\r" + "Generating response " + animation[i % len(animation)])
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write("\r" + " " * 30 + "\r")
    sys.stdout.flush()

def get_persona_description(persona_manager, persona_name):
    """Get a short description of the persona"""
    persona = persona_manager.get_persona(persona_name)
    description = getattr(persona, 'description', 'No description available')
    traits = getattr(persona, 'personality_traits', [])
    expertise = getattr(persona, 'expertise_areas', [])
    
    return {
        'description': description,
        'traits': traits,
        'expertise': expertise
    }

def main():
    """Main application entry point"""
    # Load environment variables
    load_dotenv()
    
    # Setup logging
    logger = setup_logger()
    logger.info("Starting Vantage AI PersonaPilot...")
    
    # Initialize configuration
    config = Config()
    
    # Initialize AI client
    ai_client = AIClient()
    
    # Initialize persona manager and output formatter
    persona_manager = PersonaManager(ai_client)
    output_formatter = OutputFormatter()
    
    # CLI interface
    print("\n🧠 Vantage AI PersonaPilot")
    print("=" * 40)
    
    # List available personas
    personas = persona_manager.list_personas()
    print("\n📋 Available personas:")
    for i, persona in enumerate(personas, 1):
        print(f"  {i}. {persona}")
    
    # Persona selection
    while True:
        try:
            selection = input("\n🔍 Select a persona (enter number): ")
            persona_index = int(selection) - 1
            if 0 <= persona_index < len(personas):
                persona_name = personas[persona_index]
                break
            else:
                print(f"⚠️  Please enter a number between 1 and {len(personas)}")
        except ValueError:
            print("⚠️  Please enter a valid number")
    
    # Display persona info
    persona_info = get_persona_description(persona_manager, persona_name)
    print(f"\n🎭 Selected persona: {persona_name}")
    print(f"📝 Description: {persona_info['description']}")
    
    if persona_info['traits']:
        print("🧩 Personality traits:")
        for trait in persona_info['traits']:
            print(f"  • {trait}")
    
    if persona_info['expertise']:
        print("🔧 Expertise areas:")
        for area in persona_info['expertise']:
            print(f"  • {area}")
    
    # Get user prompt
    query = input("\n💬 Enter your prompt: ")
    
    print("\n⏳ Generating response...")
    display_loading_animation(2)  # Display loading animation for 2 seconds
    
    try:
        # Get raw response from persona manager - use 'raw' output format to get the dictionary
        raw_response = persona_manager.get_response(persona_name, query, output_format="raw")
        
        # Format the response using a more readable approach
        formatted_response = ""
        
        # Check if response is a dictionary
        if isinstance(raw_response, dict):
            for key, value in raw_response.items():
                # Format section header
                section_header = key.replace('_', ' ').title()
                formatted_response += f"\n## {section_header}\n"
                
                # Format section content based on type
                if isinstance(value, list):
                    for item in value:
                        if isinstance(item, dict):
                            # Format dictionary items in a list
                            formatted_response += "\n"
                            for item_key, item_value in item.items():
                                # Handle complex nested structures
                                if isinstance(item_value, dict):
                                    # Format nested dictionary as a readable description
                                    nested_str = "\n    "
                                    for k, v in item_value.items():
                                        k_formatted = k.replace('_', ' ').title()
                                        if isinstance(v, (dict, list)):
                                            v = str(v).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                        nested_str += f"{k_formatted}: {v}\n    "
                                    item_value_str = nested_str
                                elif isinstance(item_value, list):
                                    # Format list as comma-separated values
                                    items = []
                                    for i in item_value:
                                        if isinstance(i, (dict, list)):
                                            i = str(i).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                        items.append(str(i))
                                    item_value_str = ", ".join(items)
                                else:
                                    item_value_str = str(item_value)
                                formatted_response += f"**{item_key.replace('_', ' ').title()}**: {item_value_str}\n"
                        else:
                            # Format simple list items
                            formatted_response += f"- {item}\n"
                elif isinstance(value, dict):
                    # Format nested dictionary
                    for sub_key, sub_value in value.items():
                        sub_key_formatted = sub_key.replace('_', ' ').title()
                        
                        # Handle complex nested structures
                        if isinstance(sub_value, dict):
                            # Format nested dictionary as a readable description
                            formatted_response += f"**{sub_key_formatted}**:\n"
                            for k, v in sub_value.items():
                                k_formatted = k.replace('_', ' ').title()
                                if isinstance(v, (dict, list)):
                                    v = str(v).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                formatted_response += f"    **{k_formatted}**: {v}\n"
                        elif isinstance(sub_value, list):
                            # Format list items properly
                            formatted_response += f"**{sub_key_formatted}**:\n"
                            for item in sub_value:
                                if isinstance(item, dict):
                                    formatted_response += "    - "
                                    item_parts = []
                                    for k, v in item.items():
                                        k_formatted = k.replace('_', ' ').title()
                                        if isinstance(v, (dict, list)):
                                            v = str(v).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                        item_parts.append(f"{k_formatted}: {v}")
                                    formatted_response += ", ".join(item_parts) + "\n"
                                else:
                                    formatted_response += f"    - {item}\n"
                        else:
                            # Format simple values
                            formatted_response += f"**{sub_key_formatted}**: {sub_value}\n"
                else:
                    # Format simple values
                    formatted_response += f"{value}\n"
        else:
            # If not a dictionary, just convert to string
            formatted_response = str(raw_response)
            
        print(f"\n✅ Response:\n{formatted_response}")
    except Exception as e:
        logger.error(f"Error getting response: {e}")
        print(f"❌ Error: {e}")
    
    # Ask if user wants to continue with another prompt or change persona
    while True:
        print("\n📋 Options:")
        print("  1️⃣  Ask another question with the same persona")
        print("  2️⃣  Change persona")
        print("  3️⃣  Exit")
        
        choice = input("\n🔍 Enter your choice (1-3): ")
        
        if choice == '1':
            # Ask another question with the same persona
            query = input("\n💬 Enter your prompt: ")
            print("\n⏳ Generating response...")
            display_loading_animation(2)  # Display loading animation for 2 seconds
            try:
                # Get raw response from persona manager - use 'raw' output format to get the dictionary
                raw_response = persona_manager.get_response(persona_name, query, output_format="raw")
                
                # Format the response using a more readable approach
                formatted_response = ""
                
                # Check if response is a dictionary
                if isinstance(raw_response, dict):
                    for key, value in raw_response.items():
                        # Format section header
                        section_header = key.replace('_', ' ').title()
                        formatted_response += f"\n## {section_header}\n"
                        
                        # Format section content based on type
                        if isinstance(value, list):
                            for item in value:
                                if isinstance(item, dict):
                                    # Format dictionary items in a list
                                    formatted_response += "\n"
                                    for item_key, item_value in item.items():
                                        # Handle complex nested structures
                                        if isinstance(item_value, dict):
                                            # Format nested dictionary as a readable description
                                            nested_str = "\n    "
                                            for k, v in item_value.items():
                                                k_formatted = k.replace('_', ' ').title()
                                                if isinstance(v, (dict, list)):
                                                    v = str(v).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                                nested_str += f"{k_formatted}: {v}\n    "
                                            item_value_str = nested_str
                                        elif isinstance(item_value, list):
                                            # Format list as comma-separated values
                                            items = []
                                            for i in item_value:
                                                if isinstance(i, (dict, list)):
                                                    i = str(i).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                                items.append(str(i))
                                            item_value_str = ", ".join(items)
                                        else:
                                            item_value_str = str(item_value)
                                        formatted_response += f"**{item_key.replace('_', ' ').title()}**: {item_value_str}\n"
                                else:
                                    # Format simple list items
                                    formatted_response += f"- {item}\n"
                        elif isinstance(value, dict):
                            # Format nested dictionary
                            for sub_key, sub_value in value.items():
                                sub_key_formatted = sub_key.replace('_', ' ').title()
                                
                                # Handle complex nested structures
                                if isinstance(sub_value, dict):
                                    # Format nested dictionary as a readable description
                                    formatted_response += f"**{sub_key_formatted}**:\n"
                                    for k, v in sub_value.items():
                                        k_formatted = k.replace('_', ' ').title()
                                        if isinstance(v, (dict, list)):
                                            v = str(v).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                        formatted_response += f"    **{k_formatted}**: {v}\n"
                                elif isinstance(sub_value, list):
                                    # Format list items properly
                                    formatted_response += f"**{sub_key_formatted}**:\n"
                                    for item in sub_value:
                                        if isinstance(item, dict):
                                            formatted_response += "    - "
                                            item_parts = []
                                            for k, v in item.items():
                                                k_formatted = k.replace('_', ' ').title()
                                                if isinstance(v, (dict, list)):
                                                    v = str(v).replace('{', '').replace('}', '').replace('[', '').replace(']', '').replace("'", "")
                                                item_parts.append(f"{k_formatted}: {v}")
                                            formatted_response += ", ".join(item_parts) + "\n"
                                        else:
                                            formatted_response += f"    - {item}\n"
                                else:
                                    # Format simple values
                                    formatted_response += f"**{sub_key_formatted}**: {sub_value}\n"
                        else:
                            # Format simple values
                            formatted_response += f"{value}\n"
                else:
                    # If not a dictionary, just convert to string
                    formatted_response = str(raw_response)
                    
                print(f"\n✅ Response:\n{formatted_response}")
            except Exception as e:
                logger.error(f"Error getting response: {e}")
                print(f"❌ Error: {e}")
                
        elif choice == '2':
            # Change persona
            print("\n📋 Available personas:")
            for i, persona in enumerate(personas, 1):
                print(f"  {i}. {persona}")
            
            # Persona selection
            while True:
                try:
                    selection = input("\n🔍 Select a persona (enter number): ")
                    persona_index = int(selection) - 1
                    if 0 <= persona_index < len(personas):
                        persona_name = personas[persona_index]
                        break
                    else:
                        print(f"⚠️  Please enter a number between 1 and {len(personas)}")
                except ValueError:
                    print("⚠️  Please enter a valid number")
            
            # Display persona info
            persona_info = get_persona_description(persona_manager, persona_name)
            print(f"\n🎭 Selected persona: {persona_name}")
            print(f"📝 Description: {persona_info['description']}")
            
            if persona_info['traits']:
                print("🧩 Personality traits:")
                for trait in persona_info['traits']:
                    print(f"  • {trait}")
            
            if persona_info['expertise']:
                print("🔧 Expertise areas:")
                for area in persona_info['expertise']:
                    print(f"  • {area}")
            
            # Get user prompt
            query = input("\n💬 Enter your prompt: ")
            
            print("\n⏳ Generating response...")
            display_loading_animation(2)  # Display loading animation for 2 seconds
            
            try:
                response = persona_manager.get_response(persona_name, query)
                print(f"\n✅ Response:\n{response}")
            except Exception as e:
                logger.error(f"Error getting response: {e}")
                print(f"❌ Error: {e}")
                
        elif choice == '3':
            # Exit
            print("\n👋 Thank you for using Vantage AI PersonaPilot!")
            break
            
        else:
            print("⚠️  Please enter a valid option (1-3)")

if __name__ == "__main__":
    main()
