"""
AI Module - OpenAI ChatGPT Integration

Provides AI-powered chat interface for statistics questions and analysis.
"""

from .assistant import AIAssistant, render_ai_chat, render_ai_sidebar

__all__ = ['AIAssistant', 'render_ai_chat', 'render_ai_sidebar']
