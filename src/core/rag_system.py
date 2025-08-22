"""
RAG (Retrieval-Augmented Generation) System for Vantage AI PersonaPilot
"""

from typing import List, Dict, Any, Optional
import logging
import os
import json

logger = logging.getLogger(__name__)

class RAGSystem:
    """Retrieval-Augmented Generation system for enhanced responses"""
    
    def __init__(self, vector_db_path: str = "data/vector_db"):
        self.vector_db_path = vector_db_path
        self.documents = []
        self.embeddings = None
        self.vector_index = None
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the RAG system"""
        try:
            # Create vector DB directory if it doesn't exist
            os.makedirs(self.vector_db_path, exist_ok=True)
            
            # Load existing documents if available
            self._load_documents()
            
            logger.info("RAG system initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing RAG system: {e}")
    
    def _load_documents(self):
        """Load documents from storage"""
        documents_file = os.path.join(self.vector_db_path, "documents.json")
        if os.path.exists(documents_file):
            try:
                with open(documents_file, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                logger.info(f"Loaded {len(self.documents)} documents")
            except Exception as e:
                logger.error(f"Error loading documents: {e}")
                self.documents = []
    
    def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None):
        """Add a document to the knowledge base"""
        document = {
            "id": len(self.documents),
            "content": content,
            "metadata": metadata or {}
        }
        self.documents.append(document)
        self._save_documents()
        logger.info(f"Added document {document['id']}")
    
    def _save_documents(self):
        """Save documents to storage"""
        documents_file = os.path.join(self.vector_db_path, "documents.json")
        try:
            with open(documents_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error(f"Error saving documents: {e}")
    
    def retrieve_relevant_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: Search query
            top_k: Number of documents to retrieve
            
        Returns:
            List of relevant documents
        """
        if not self.documents:
            return []
        
        # Simple keyword-based retrieval (placeholder for vector search)
        relevant_docs = []
        query_terms = query.lower().split()
        
        for doc in self.documents:
            content = doc["content"].lower()
            relevance_score = sum(1 for term in query_terms if term in content)
            
            if relevance_score > 0:
                relevant_docs.append({
                    "document": doc,
                    "relevance_score": relevance_score
                })
        
        # Sort by relevance and return top_k
        relevant_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        return [doc["document"] for doc in relevant_docs[:top_k]]
    
    def get_context_for_query(self, query: str, max_length: int = 1000) -> Optional[str]:
        """
        Get context for a query by retrieving relevant documents
        
        Args:
            query: User query
            max_length: Maximum context length
            
        Returns:
            Context string or None
        """
        relevant_docs = self.retrieve_relevant_documents(query)
        
        if not relevant_docs:
            return None
        
        # Combine relevant document content
        context_parts = []
        current_length = 0
        
        for doc in relevant_docs:
            content = doc["content"]
            if current_length + len(content) > max_length:
                break
            
            context_parts.append(content)
            current_length += len(content)
        
        if context_parts:
            return "\n\n".join(context_parts)
        
        return None
    
    def add_knowledge_base(self, knowledge_base_path: str):
        """Add documents from a knowledge base directory"""
        if not os.path.exists(knowledge_base_path):
            logger.error(f"Knowledge base path does not exist: {knowledge_base_path}")
            return
        
        # Process files in the knowledge base directory
        for filename in os.listdir(knowledge_base_path):
            file_path = os.path.join(knowledge_base_path, filename)
            
            if os.path.isfile(file_path) and filename.endswith(('.txt', '.md', '.json')):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    metadata = {
                        "source": filename,
                        "file_path": file_path
                    }
                    
                    self.add_document(content, metadata)
                    logger.info(f"Added document from {filename}")
                    
                except Exception as e:
                    logger.error(f"Error processing {filename}: {e}")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get RAG system statistics"""
        return {
            "total_documents": len(self.documents),
            "vector_db_path": self.vector_db_path,
            "system_ready": self.vector_index is not None
        }

