"""
LABBAIK AI v6.0 - RAG Service
============================
Retrieval-Augmented Generation service with ChromaDB and sentence transformers.
"""

import os
import logging
from typing import Optional, List, Dict, Any, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import json

from services.ai.base import (
    BaseChatService,
    ChatMessage,
    ChatCompletionRequest,
    ChatCompletionResponse,
    MessageRole,
)
from core.exceptions import RAGError, AIServiceError
from core.constants import Messages

logger = logging.getLogger(__name__)


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class Document:
    """Represents a document in the knowledge base."""
    id: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    embedding: Optional[List[float]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.content,
            "metadata": self.metadata,
        }


@dataclass
class RetrievalResult:
    """Result from document retrieval."""
    documents: List[Document]
    scores: List[float]
    query: str
    
    @property
    def best_match(self) -> Optional[Document]:
        """Get the best matching document."""
        return self.documents[0] if self.documents else None
    
    def get_context(self, max_docs: int = 5) -> str:
        """Get combined context from top documents."""
        docs = self.documents[:max_docs]
        return "\n\n---\n\n".join([
            f"[Sumber: {doc.metadata.get('source', 'unknown')}]\n{doc.content}"
            for doc in docs
        ])


@dataclass
class RAGResponse:
    """Response from RAG query."""
    answer: str
    context: str
    sources: List[Dict[str, Any]]
    confidence: float
    chat_response: ChatCompletionResponse


# =============================================================================
# EMBEDDING SERVICE
# =============================================================================

class LocalEmbeddingService:
    """
    Local embedding service using sentence-transformers.
    No API key required - runs on device.
    """
    
    DEFAULT_MODEL = "all-MiniLM-L6-v2"
    
    def __init__(self, model_name: str = None):
        self.model_name = model_name or self.DEFAULT_MODEL
        self._model = None
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize the embedding model."""
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            self._initialized = True
            logger.info(f"Embedding model loaded: {self.model_name}")
            return True
        except ImportError:
            logger.error("sentence-transformers not installed. Run: pip install sentence-transformers")
            return False
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            return False
    
    def _ensure_initialized(self):
        """Ensure model is initialized."""
        if not self._initialized:
            if not self.initialize():
                raise RAGError("Failed to initialize embedding model")
    
    def embed(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for texts."""
        self._ensure_initialized()
        
        try:
            embeddings = self._model.encode(texts, convert_to_numpy=True)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            raise RAGError(f"Failed to generate embeddings: {e}")
    
    def embed_single(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        return self.embed([text])[0]


# =============================================================================
# VECTOR STORE
# =============================================================================

class ChromaVectorStore:
    """
    Vector store using ChromaDB for document storage and retrieval.
    """
    
    def __init__(
        self,
        collection_name: str = "labbaik_knowledge",
        persist_directory: Optional[str] = None,
        embedding_service: Optional[LocalEmbeddingService] = None
    ):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.embedding_service = embedding_service or LocalEmbeddingService()
        self._client = None
        self._collection = None
        self._initialized = False
    
    def initialize(self) -> bool:
        """Initialize ChromaDB."""
        try:
            import chromadb
            from chromadb.config import Settings
            
            if self.persist_directory:
                self._client = chromadb.PersistentClient(
                    path=self.persist_directory,
                    settings=Settings(anonymized_telemetry=False)
                )
            else:
                self._client = chromadb.Client(
                    settings=Settings(anonymized_telemetry=False)
                )
            
            self._collection = self._client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "LABBAIK AI Knowledge Base"}
            )
            
            # Initialize embedding service
            self.embedding_service.initialize()
            
            self._initialized = True
            logger.info(f"ChromaDB initialized: {self.collection_name}")
            return True
            
        except ImportError:
            logger.error("chromadb not installed. Run: pip install chromadb")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {e}")
            return False
    
    def _ensure_initialized(self):
        """Ensure store is initialized."""
        if not self._initialized:
            if not self.initialize():
                raise RAGError("Failed to initialize vector store")
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID for content."""
        return hashlib.md5(content.encode()).hexdigest()
    
    def add_documents(
        self,
        documents: List[Document],
        batch_size: int = 100
    ) -> int:
        """Add documents to the vector store."""
        self._ensure_initialized()
        
        added = 0
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            ids = [doc.id or self._generate_id(doc.content) for doc in batch]
            contents = [doc.content for doc in batch]
            metadatas = [doc.metadata for doc in batch]
            
            # Generate embeddings
            embeddings = self.embedding_service.embed(contents)
            
            # Add to collection
            self._collection.add(
                ids=ids,
                documents=contents,
                embeddings=embeddings,
                metadatas=metadatas
            )
            
            added += len(batch)
            logger.debug(f"Added {added}/{len(documents)} documents")
        
        logger.info(f"Added {added} documents to vector store")
        return added
    
    def add_texts(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ) -> int:
        """Add texts to the vector store."""
        documents = []
        for i, text in enumerate(texts):
            doc = Document(
                id=ids[i] if ids else self._generate_id(text),
                content=text,
                metadata=metadatas[i] if metadatas else {}
            )
            documents.append(doc)
        
        return self.add_documents(documents)
    
    def search(
        self,
        query: str,
        top_k: int = 5,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> RetrievalResult:
        """Search for similar documents."""
        self._ensure_initialized()
        
        try:
            # Generate query embedding
            query_embedding = self.embedding_service.embed_single(query)
            
            # Search
            results = self._collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=filter_metadata
            )
            
            # Parse results
            documents = []
            scores = []
            
            if results["ids"] and results["ids"][0]:
                for i, doc_id in enumerate(results["ids"][0]):
                    doc = Document(
                        id=doc_id,
                        content=results["documents"][0][i] if results["documents"] else "",
                        metadata=results["metadatas"][0][i] if results["metadatas"] else {}
                    )
                    documents.append(doc)
                    
                    # Convert distance to similarity score (1 - distance for L2)
                    if results["distances"]:
                        score = 1 - (results["distances"][0][i] / 2)  # Normalize
                        scores.append(max(0, min(1, score)))
                    else:
                        scores.append(1.0)
            
            return RetrievalResult(
                documents=documents,
                scores=scores,
                query=query
            )
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise RAGError(f"Search failed: {e}")
    
    def delete(self, ids: List[str]) -> int:
        """Delete documents by ID."""
        self._ensure_initialized()
        
        try:
            self._collection.delete(ids=ids)
            logger.info(f"Deleted {len(ids)} documents")
            return len(ids)
        except Exception as e:
            logger.error(f"Delete failed: {e}")
            return 0
    
    def count(self) -> int:
        """Get document count."""
        self._ensure_initialized()
        return self._collection.count()
    
    def clear(self) -> bool:
        """Clear all documents."""
        self._ensure_initialized()
        
        try:
            self._client.delete_collection(self.collection_name)
            self._collection = self._client.create_collection(
                name=self.collection_name,
                metadata={"description": "LABBAIK AI Knowledge Base"}
            )
            logger.info("Vector store cleared")
            return True
        except Exception as e:
            logger.error(f"Clear failed: {e}")
            return False


# =============================================================================
# RAG SERVICE
# =============================================================================

class RAGService:
    """
    Retrieval-Augmented Generation service.
    Combines vector retrieval with LLM for context-aware responses.
    """
    
    RAG_SYSTEM_PROMPT = """Anda adalah LABBAIK AI, asisten cerdas untuk perencanaan ibadah Umrah.

Gunakan konteks berikut untuk menjawab pertanyaan pengguna. Jika informasi tidak ada dalam konteks, 
katakan bahwa Anda tidak memiliki informasi tersebut dan sarankan untuk mencari dari sumber terpercaya.

KONTEKS:
{context}

INSTRUKSI:
1. Jawab berdasarkan konteks yang diberikan
2. Jika konteks tidak cukup, katakan dengan jujur
3. Gunakan bahasa Indonesia yang baik dan santun
4. Sertakan referensi sumber jika relevan
5. Dorong pengguna untuk DYOR (Do Your Own Research)"""
    
    def __init__(
        self,
        chat_service: BaseChatService,
        vector_store: Optional[ChromaVectorStore] = None,
        top_k: int = 5,
        min_confidence: float = 0.5
    ):
        self.chat_service = chat_service
        self.vector_store = vector_store or ChromaVectorStore()
        self.top_k = top_k
        self.min_confidence = min_confidence
    
    def initialize(self) -> bool:
        """Initialize RAG service."""
        try:
            self.chat_service.initialize()
            self.vector_store.initialize()
            return True
        except Exception as e:
            logger.error(f"RAG initialization failed: {e}")
            return False
    
    def query(
        self,
        question: str,
        chat_history: Optional[List[ChatMessage]] = None,
        filter_metadata: Optional[Dict[str, Any]] = None
    ) -> RAGResponse:
        """
        Query the RAG system.
        
        Args:
            question: User's question
            chat_history: Previous chat messages for context
            filter_metadata: Metadata filter for retrieval
        
        Returns:
            RAGResponse with answer and sources
        """
        # Retrieve relevant documents
        retrieval = self.vector_store.search(
            query=question,
            top_k=self.top_k,
            filter_metadata=filter_metadata
        )
        
        # Get context from top documents
        context = retrieval.get_context(max_docs=self.top_k)
        
        # Calculate confidence based on scores
        confidence = (
            sum(retrieval.scores[:3]) / min(3, len(retrieval.scores))
            if retrieval.scores else 0.0
        )
        
        # Build messages
        messages = []
        
        # System prompt with context
        system_prompt = self.RAG_SYSTEM_PROMPT.format(context=context)
        messages.append(ChatMessage.system(system_prompt))
        
        # Add chat history
        if chat_history:
            for msg in chat_history[-6:]:  # Last 6 messages
                messages.append(msg)
        
        # Add current question
        messages.append(ChatMessage.user(question))
        
        # Generate response
        request = ChatCompletionRequest(
            messages=messages,
            temperature=0.7,
            max_tokens=2048
        )
        
        chat_response = self.chat_service.complete(request)
        
        # Build sources list
        sources = [
            {
                "content": doc.content[:200] + "...",
                "source": doc.metadata.get("source", "unknown"),
                "score": retrieval.scores[i] if i < len(retrieval.scores) else 0
            }
            for i, doc in enumerate(retrieval.documents[:3])
        ]
        
        return RAGResponse(
            answer=chat_response.content,
            context=context,
            sources=sources,
            confidence=confidence,
            chat_response=chat_response
        )
    
    def add_knowledge(
        self,
        texts: List[str],
        source: str = "manual",
        category: Optional[str] = None
    ) -> int:
        """
        Add knowledge to the RAG system.
        
        Args:
            texts: List of text chunks to add
            source: Source identifier
            category: Category for filtering
        
        Returns:
            Number of documents added
        """
        metadatas = [
            {"source": source, "category": category or "general"}
            for _ in texts
        ]
        
        return self.vector_store.add_texts(texts, metadatas)
    
    def load_knowledge_file(
        self,
        file_path: str,
        chunk_size: int = 500,
        chunk_overlap: int = 50
    ) -> int:
        """
        Load knowledge from a text file.
        
        Args:
            file_path: Path to text file
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        
        Returns:
            Number of chunks added
        """
        path = Path(file_path)
        if not path.exists():
            raise RAGError(f"File not found: {file_path}")
        
        content = path.read_text(encoding="utf-8")
        
        # Simple chunking
        chunks = self._chunk_text(content, chunk_size, chunk_overlap)
        
        return self.add_knowledge(
            texts=chunks,
            source=path.name,
            category=path.stem
        )
    
    def _chunk_text(
        self,
        text: str,
        chunk_size: int,
        overlap: int
    ) -> List[str]:
        """Split text into overlapping chunks."""
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            # Try to break at sentence boundary
            if end < len(text):
                last_period = chunk.rfind(".")
                if last_period > chunk_size // 2:
                    end = start + last_period + 1
                    chunk = text[start:end]
            
            chunks.append(chunk.strip())
            start = end - overlap
        
        return [c for c in chunks if c]  # Remove empty chunks
    
    def get_stats(self) -> Dict[str, Any]:
        """Get RAG system statistics."""
        return {
            "document_count": self.vector_store.count(),
            "top_k": self.top_k,
            "min_confidence": self.min_confidence,
            "chat_provider": self.chat_service.provider_name,
        }
