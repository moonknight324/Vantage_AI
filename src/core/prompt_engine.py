"""
Prompt Engineering for Vantage AI PersonaPilot
"""

from typing import Dict, Any, List, Optional
import json
import logging

logger = logging.getLogger(__name__)

class PromptEngine:
    """Dynamic prompt engineering for persona-driven responses"""
    
    def __init__(self):
        self.prompt_templates = {}
        self.few_shot_examples = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize prompt templates"""
        # This method defines templates for different prompting techniques:
        # - zero_shot: Zero-shot prompting (no examples)
        # - one_shot: One-shot prompting (single example)
        # - few_shot: Few-shot prompting (multiple examples)
        # - rag_enhanced: Retrieval-augmented generation with context
        # - structured: Structured output format
        self.prompt_templates = {
            "zero_shot": "{system_prompt}\n\nUser Query: {query}",
            "one_shot": "{system_prompt}\n\nExample:\n{example}\n\nUser Query: {query}",
            "few_shot": "{system_prompt}\n\nExamples:\n{examples}\n\nUser Query: {query}",
            "rag_enhanced": "{system_prompt}\n\nContext: {context}\n\nUser Query: {query}",
            "structured": "{system_prompt}\n\nUser Query: {query}\n\nPlease respond in the following format: {output_format}"
        }
    
    def create_prompt(self, 
                     prompt_type: str,
                     system_prompt: str,
                     query: str,
                     context: Optional[str] = None,
                     examples: Optional[List[str]] = None,
                     output_format: Optional[Dict[str, Any]] = None,
                     persona_preferences: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a dynamic prompt based on type and parameters
        
        Args:
            prompt_type: Type of prompt (zero_shot, one_shot, few_shot, rag_enhanced, structured)
            system_prompt: System prompt for the persona
            query: User's query
            context: Optional context from RAG
            examples: Optional examples for few-shot learning
            output_format: Optional output format specification
            
        Returns:
            Formatted prompt string
        """
        template = self.prompt_templates.get(prompt_type, self.prompt_templates["zero_shot"])
        
        # Prepare template variables
        variables = {
            "system_prompt": system_prompt,
            "query": query
        }
        
        if context:
            variables["context"] = context
        
        if examples:
            if prompt_type == "one_shot" and len(examples) > 0:
                variables["example"] = examples[0]
            elif prompt_type == "few_shot":
                variables["examples"] = "\n\n".join(examples)
        
        if output_format:
            variables["output_format"] = json.dumps(output_format, indent=2)
        
        # Format the prompt
        try:
            prompt = template.format(**variables)
            logger.debug(f"Created {prompt_type} prompt")
            return prompt
        except KeyError as e:
            logger.error(f"Missing template variable: {e}")
            return self.prompt_templates["zero_shot"].format(**variables)
    
    def create_dynamic_prompt(self,
                            persona_prompt: str,
                            query: str,
                            context: Optional[str] = None,
                            complexity: str = "medium",
                            output_format: Optional[str] = None) -> str:
        """
        Create a dynamic prompt that adapts based on query complexity
        
        This method implements dynamic prompting by selecting different prompting techniques
        based on query complexity and available context
        
        Args:
            persona_prompt: Base persona system prompt
            query: User's query
            context: Optional RAG context
            complexity: Query complexity (simple, medium, complex)
            output_format: Desired output format
            
        Returns:
            Dynamic prompt string
        """
        # This method implements dynamic prompting by selecting different prompting techniques
        # based on query complexity and available context
        # Determine prompt type based on complexity and context
        if context:
            prompt_type = "rag_enhanced"
        elif complexity == "complex":
            prompt_type = "few_shot"
        elif complexity == "medium":
            prompt_type = "one_shot"
        else:
            prompt_type = "zero_shot"
        
        # Get examples if needed
        examples = None
        if prompt_type in ["one_shot", "few_shot"]:
            examples = self._get_relevant_examples(query, complexity)
        
        # Create the prompt
        return self.create_prompt(
            prompt_type=prompt_type,
            system_prompt=persona_prompt,
            query=query,
            context=context,
            examples=examples,
            output_format=output_format
        )
    
    def _get_relevant_examples(self, query: str, complexity: str) -> List[str]:
        """Get relevant examples for few-shot learning"""
        # This would be implemented to retrieve relevant examples
        # For now, return basic examples
        return [
            "Example 1: Basic response example",
            "Example 2: More detailed response example"
        ]
    
    def optimize_prompt(self, prompt: str, max_length: int = 4000) -> str:
        """Optimize prompt length and structure"""
        if len(prompt) <= max_length:
            return prompt
        
        # Simple optimization: truncate context if too long
        lines = prompt.split('\n')
        optimized_lines = []
        current_length = 0
        
        for line in lines:
            if current_length + len(line) > max_length:
                break
            optimized_lines.append(line)
            current_length += len(line) + 1  # +1 for newline
        
        return '\n'.join(optimized_lines)

