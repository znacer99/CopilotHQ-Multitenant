from .base import BaseAgent
from django.db import connection
import logging

logger = logging.getLogger(__name__)

class KnowledgeAgent(BaseAgent):
    agent_type = "knowledge"
    
    def build_context(self):
        base_context = super().build_context()
        return f"""
{base_context}
YOUR ROLE:
You are the Knowledge Agent. Your purpose is to be the intelligent search layer for the company.
Your responsibilities include:
- Finding information within company documents (PDFs, handbooks, etc.).
- Summarizing complex policies.
- Answering questions based ONLY on provided factual data.
- Helping employees find where specific HR or IT policies are stored.

TOOLS AVAILABLE:
- search_documents(query): Search through the company knowledge base for relevant snippets.
- summarize_policy(document_id): Provide a concise summary of a specific document.
- list_categories(): List all available document categories (e.g., Benefits, Compliance, IT).

TONE:
Factual, precise, and objective. If information is missing from the documents, state that you do not know.
"""

    def search_knowledge(self, query):
        """Perform keyword search over the KnowledgeBase"""
        from .models import KnowledgeBase
        from django.db.models import Q
        
        # Simple keyword search across content and title
        results = KnowledgeBase.objects.filter(
            tenant=self.tenant,
            is_active=True
        ).filter(
            Q(content__icontains=query) | Q(title__icontains=query)
        )[:5]
        
        if not results.exists():
            return {
                "query": query,
                "results": [],
                "summary": "No documents found matching your query in the company knowledge base."
            }

        formatted_results = []
        context_text = ""
        for res in results:
            # Create a snippet from content
            snippet = res.content[:200] + "..." if len(res.content) > 200 else res.content
            formatted_results.append({
                "title": res.title,
                "snippet": snippet,
                "relevance": 1.0 # Simple match
            })
            context_text += f"\nDocument: {res.title}\nContent: {res.content[:1000]}\n"

        if self.mock_mode:
            return {
                "query": query,
                "results": formatted_results,
                "summary": f"Found {len(formatted_results)} relevant documents. Summarizing based on match..."
            }
            
        # Real Claude call with extracted context
        prompt = f"""
Using the following company documents, answer the user's question.
If the information is not present, say you don't know based on the documents.

DOCUMENTS:
{context_text}

USER QUESTION: {query}
"""
        return self.call_claude(prompt)

    def ingest_document(self, file_path, title, category="General"):
        """Extracts text from a file and saves to KnowledgeBase"""
        from .models import KnowledgeBase
        import os
        
        content = ""
        ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if ext == '.pdf':
                from PyPDF2 import PdfReader
                reader = PdfReader(file_path)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
            else:
                # Treat as plain text
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            
            kb_entry, created = KnowledgeBase.objects.update_or_create(
                tenant=self.tenant,
                title=title,
                defaults={'content': content, 'category': category}
            )
            return {"success": True, "title": title, "created": created}
        except Exception as e:
            logger.error(f"Failed to ingest document {title}: {str(e)}")
            return {"success": False, "error": str(e)}

    def get_document_summary(self, doc_id):
        """Returns a summary of a document"""
        if self.mock_mode:
            return {
                "doc_id": doc_id,
                "title": "Security Policy.pdf",
                "summary": "This document outlines the mandatory use of 2FA and password complexity requirements.",
                "last_updated": "2025-11-20"
            }
        
        prompt = f"Summarize the document with ID {doc_id}."
        return self.call_claude(prompt)
