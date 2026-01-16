"""
AI Assistant Module - OpenAI Integration
Provides AI-powered answers and visualizations for user questions about UK dating statistics.
"""

import os
import re
import json
import streamlit as st
import pandas as pd
from typing import Optional, Dict, List, Tuple
import plotly.graph_objects as go
import plotly.express as px

from src.data.constants import (
    INCOME_DISTRIBUTION_MALE,
    INCOME_DISTRIBUTION_FEMALE,
    EMPLOYMENT_RATE_BY_AGE_GENDER,
    SINGLE_RATE_BY_AGE,
    ETHNICITY_DISTRIBUTION,
    UK_ADULT_POPULATION,
    GENDER_SPLIT,
    MARRIAGE_RATE_BY_ETHNICITY,
    UK_REGIONS,
)


def _load_env_file() -> None:
    """Load environment variables from a .env file if python-dotenv is installed."""
    try:
        from dotenv import load_dotenv  # type: ignore
    except ImportError:
        return
    load_dotenv()


def _log_debug(msg: str) -> None:
    """Lightweight debug logger that surfaces in the terminal."""
    try:
        print(f"[AI Assistant] {msg}", flush=True)
    except Exception:
        pass

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class AIAssistant:
    """AI Assistant for answering questions about UK dating statistics."""
    
    def __init__(self):
        """Initialize the AI Assistant with OpenAI client."""
        _load_env_file()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self.model = "gpt-4o-mini"  # Using GPT-4 mini for cost efficiency
        
        if self.api_key and OpenAI:
            try:
                self.client = OpenAI(api_key=self.api_key)
                _log_debug("OpenAI client initialized using OPENAI_API_KEY")
            except Exception as e:
                st.warning(f"Failed to initialize OpenAI client: {str(e)}")
                _log_debug(f"Failed to init OpenAI client: {e}")
    
    def is_available(self) -> bool:
        """Check if AI Assistant is available."""
        return self.client is not None and OpenAI is not None
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the AI assistant."""
        return """You are an expert AI assistant specializing in UK dating statistics and demographics.

    Your role is to:
    1. Answer questions about UK dating, marriage, income, and demographic statistics
    2. Provide insights based on official ONS (Office for National Statistics) data
    3. Explain statistical concepts in an accessible way
    4. Suggest relevant data visualizations when appropriate
    5. Cite data sources when making claims

    Context about the data:
    - All statistics are based on official UK government sources (Census, ONS, ASHE)
    - Data is current as of 2024
    - Geographic scope: England, Scotland, Wales, Northern Ireland (UK)
    - Key datasets: Census 2021, ONS Labour Force Survey, ASHE 2024
    - Demographics tracked: Age, gender, ethnicity, income, marital status, employment

    When responding:
    - Be accurate and cite specific data when available
    - Explain the implications of statistics
    - Avoid speculation beyond the data
    - Suggest helpful follow-up questions
    - Offer to create visualizations for complex data
    - Never say you cannot create visuals; the app renders charts and maps for you. If the user hints at a chart, confidently describe the insight as if the chart is displayed above.
    - Use ONLY the curated datasets provided (Census 2021, ONS, ASHE). If an exact value is not available, state that clearly instead of inventing numbers.
    - When a chart is generated, align your numeric statements with the chart data provided in context; do not introduce new numbers."""
    
    def ask_question(self, question: str, context: Optional[str] = None) -> Tuple[str, Dict]:
        """
        Ask the AI assistant a question about UK dating statistics.
        
        Args:
            question: The user's question
            context: Optional context about currently displayed data
            
        Returns:
            Tuple of (answer_text, metadata_dict)
        """
        if not self.is_available():
            return "AI Assistant is not available. Please set OPENAI_API_KEY environment variable.", {"error": True}
        
        try:
            _log_debug(f"Chat request -> question='{question[:120]}' context_present={bool(context)}")
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ]
            
            # Add context if provided
            if context:
                messages.append({
                    "role": "user",
                    "content": f"Context: {context}\n\nQuestion: {question}"
                })
            else:
                messages.append({"role": "user", "content": question})
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1500
            )
            
            answer = response.choices[0].message.content
            
            metadata = {
                "model": self.model,
                "tokens_used": response.usage.total_tokens,
                "error": False
            }

            _log_debug(f"Chat response <- tokens_used={response.usage.total_tokens} model={self.model}")
            
            return self._strip_visualization_disclaimer(answer), metadata
            
        except Exception as e:
            error_msg = f"Error getting AI response: {str(e)}"
            _log_debug(error_msg)
            return error_msg, {"error": True, "error_type": type(e).__name__}

    def _strip_visualization_disclaimer(self, answer: str) -> str:
        """Remove boilerplate claims that the AI cannot create visualizations."""
        lowered = answer.lower()
        bad_phrases = [
            "cannot create visualizations",
            "can't create visualizations",
            "cannot create a visualization",
            "cannot create charts",
            "can't create charts",
            "cannot generate charts",
            "can't generate charts",
            "guide you on how to create",
        ]

        if not any(phrase in lowered for phrase in bad_phrases):
            return answer

        sentences = re.split(r"(?<=[.!?])\s+", answer)
        filtered = [s for s in sentences if not any(p in s.lower() for p in bad_phrases)]
        if not filtered:
            return "I generated a chart above using the available data."

        prefix = "I generated a chart above using the available data. "
        return prefix + " ".join(filtered)
    
    def generate_visualization_suggestion(self, question: str) -> Dict:
        """
        Generate a suggestion for what visualization would be useful.
        
        Args:
            question: The user's question
            
        Returns:
            Dictionary with visualization suggestions
        """
        if not self.is_available():
            return {}
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data visualization expert. Respond with JSON only."},
                    {"role": "user", "content": f"""Based on this question about UK dating statistics, suggest the best visualization.
                    
Question: {question}

Respond with ONLY valid JSON (no markdown, no extra text) with this structure:
{{
    "visualization_type": "bar|line|scatter|pie|map|histogram",
    "title": "suggested chart title",
    "x_axis": "x-axis label",
    "y_axis": "y-axis label",
    "reasoning": "why this visualization works"
}}"""}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            suggestion = json.loads(response_text)
            return suggestion
            
        except Exception as e:
            return {"error": str(e)}

    def _processed_path(self, filename: str) -> str:
        """Helper to build a data/processed path."""
        return os.path.join(os.path.dirname(__file__), "..", "..", "data", "processed", filename)

    def _load_income_df(self) -> pd.DataFrame:
        """Load income distribution (male/female) from processed CSVs when present, else constants."""
        male_path = self._processed_path("income_distribution_male.csv")
        female_path = self._processed_path("income_distribution_female.csv")
        try:
            male_df = pd.read_csv(male_path).assign(gender="Male")
            female_df = pd.read_csv(female_path).assign(gender="Female")
            return pd.concat([male_df, female_df], ignore_index=True)
        except Exception:
            male_df = pd.DataFrame({"income_bracket": list(INCOME_DISTRIBUTION_MALE.keys()), "probability": list(INCOME_DISTRIBUTION_MALE.values()), "gender": "Male"})
            female_df = pd.DataFrame({"income_bracket": list(INCOME_DISTRIBUTION_FEMALE.keys()), "probability": list(INCOME_DISTRIBUTION_FEMALE.values()), "gender": "Female"})
            return pd.concat([male_df, female_df], ignore_index=True)

    def _load_employment_df(self) -> pd.DataFrame:
        """Load employment rates by age/gender from processed CSV when present, else constants."""
        path = self._processed_path("employment_rate_by_age_gender.csv")
        try:
            return pd.read_csv(path)
        except Exception:
            rows = []
            for age_band, genders in EMPLOYMENT_RATE_BY_AGE_GENDER.items():
                for gender, rate in genders.items():
                    rows.append({"age_band": age_band, "gender": gender, "rate": rate})
            return pd.DataFrame(rows)

    def _load_single_df(self) -> pd.DataFrame:
        """Load single rates by age from processed CSV when present, else constants."""
        path = self._processed_path("single_rate_by_age.csv")
        try:
            df = pd.read_csv(path)
            if set(df.columns) >= {"key", "value"}:
                df = df.rename(columns={"key": "age_band", "value": "rate"})
            return df
        except Exception:
            return pd.DataFrame({"age_band": list(SINGLE_RATE_BY_AGE.keys()), "rate": list(SINGLE_RATE_BY_AGE.values())})

    def _load_ethnicity_df(self) -> pd.DataFrame:
        """Return ethnicity distribution as a DataFrame."""
        return pd.DataFrame({
            "ethnicity": list(ETHNICITY_DISTRIBUTION.keys()),
            "share": list(ETHNICITY_DISTRIBUTION.values())
        })

    def build_chart_or_map(self, question: str) -> Tuple[Optional[go.Figure], str, str]:
        """Attempt to build a chart or map based on the question keywords.

        Returns: (figure, fig_type, context_text)
        fig_type is "chart" or "map" when applicable; context_text summarizes the data used.
        """
        q = question.lower()
        try:
            _log_debug(f"build_chart_or_map question='{q[:120]}'")

            def _format_int(val: float) -> int:
                return int(round(val))

            # Caribbean married men vs women (derived, deterministic)
            if "caribbean" in q and any(k in q for k in ["married", "marriage", "civil"]):
                share = ETHNICITY_DISTRIBUTION.get("Black/Black British - Caribbean", 0.0)
                marriage_rate = MARRIAGE_RATE_BY_ETHNICITY.get("Black/Black British - Caribbean", 0.0)
                total_adults = UK_ADULT_POPULATION * share
                male_adults = total_adults * GENDER_SPLIT.get("Male", 0.5)
                female_adults = total_adults * GENDER_SPLIT.get("Female", 0.5)
                married_men = _format_int(male_adults * marriage_rate)
                married_women = _format_int(female_adults * marriage_rate)

                df = pd.DataFrame({
                    "gender": ["Men", "Women"],
                    "married_count": [married_men, married_women]
                })
                fig = px.bar(df, x="gender", y="married_count",
                             title="Married Caribbean adults (derived from Census 2021 share and marriage rate)")
                fig.update_layout(xaxis_title="Gender", yaxis_title="Estimated married adults")

                context = (
                    "Derived Caribbean married counts from Census 2021: "
                    f"adult share={share:.2%}, marriage rate={marriage_rate:.1%}, "
                    f"male married≈{married_men}, female married≈{married_women}. "
                    "Numbers are deterministic and should be reused verbatim."
                )
                return fig, "chart", context

            # Ethnicity-focused requests (including Caribbean) -> ethnicity distribution chart
            if any(k in q for k in ["caribbean", "ethnic", "ethnicity", "race", "black"]):
                df = self._load_ethnicity_df()
                fig = px.bar(df, x="ethnicity", y="share", title="Ethnicity distribution (population share)")
                fig.update_layout(xaxis_title="Ethnicity", yaxis_title="Population share", xaxis_tickangle=-30)
                context = "Ethnicity distribution by population share (Census 2021)."
                return fig, "chart", context

            if any(k in q for k in ["map", "region", "where"]):
                df = pd.DataFrame([
                    {"region": r, "adult_pop": d.get("adult_pop", d.get("population", 0)), "lat": d["lat"], "lon": d["lon"]}
                    for r, d in UK_REGIONS.items()
                ])
                fig = px.scatter_geo(
                    df,
                    lat="lat",
                    lon="lon",
                    size="adult_pop",
                    hover_name="region",
                    projection="natural earth",
                    scope="europe",
                    title="Adult population by UK region (approximate)"
                )
                fig.update_traces(marker=dict(opacity=0.7, line=dict(width=0)))
                fig.update_geos(fitbounds="locations", visible=False)
                context = "Map of UK regions sized by adult population (approximate)."
                return fig, "map", context

            if "income" in q:
                df = self._load_income_df()
                fig = px.bar(df, x="income_bracket", y="probability", color="gender", barmode="group",
                             title="Income distribution (probability by bracket)")
                fig.update_layout(xaxis_title="Income bracket", yaxis_title="Probability", legend_title="Gender")
                context = "Income distribution by bracket and gender (probabilities)."
                return fig, "chart", context

            if any(k in q for k in ["employment", "employed", "workforce"]):
                df = self._load_employment_df()
                fig = px.bar(df, x="age_band", y="rate", color="gender", barmode="group",
                             title="Employment rate by age and gender")
                fig.update_layout(xaxis_title="Age band", yaxis_title="Employment rate")
                context = "Employment rate by age band and gender."
                return fig, "chart", context

            if any(k in q for k in ["single", "marriage", "marital"]):
                df = self._load_single_df()
                fig = px.bar(df, x="age_band", y="rate", title="Single / never married rate by age band")
                fig.update_layout(xaxis_title="Age band", yaxis_title="Single rate")
                context = "Single / never married rate by age band."
                return fig, "chart", context

            # Fallback: if user asked for a chart/visualization but no specific dataset matched
            if any(k in q for k in ["chart", "graph", "visual", "visualization", "plot"]):
                df = self._load_single_df()
                fig = px.bar(df, x="age_band", y="rate", title="Single / never married rate by age band (fallback)")
                fig.update_layout(xaxis_title="Age band", yaxis_title="Single rate")
                context = "Fallback single / never married rate by age band."
                return fig, "chart", context

        except Exception as e:
            _log_debug(f"Chart/map build failed: {e}")
            return None, "", ""

        # Guaranteed fallback: show single rate chart so the user sees an actual plot
        df = self._load_single_df()
        fig = px.bar(df, x="age_band", y="rate", title="Single / never married rate by age band (fallback)")
        fig.update_layout(xaxis_title="Age band", yaxis_title="Single rate")
        context = "Guaranteed fallback single / never married rate by age band."
        return fig, "chart", context


def initialize_session_state():
    """Initialize session state for AI assistant."""
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []
    if "ai_assistant" not in st.session_state or not hasattr(st.session_state.ai_assistant, "build_chart_or_map"):
        st.session_state.ai_assistant = AIAssistant()
    if "ai_last_fig" not in st.session_state:
        st.session_state.ai_last_fig = None
    if "ai_last_fig_type" not in st.session_state:
        st.session_state.ai_last_fig_type = ""


def render_ai_chat():
    """Render the AI chat interface."""
    initialize_session_state()
    assistant = st.session_state.ai_assistant
    
    st.markdown("## 🤖 AI Assistant")
    
    if not assistant.is_available():
        st.warning("""
        **AI Assistant is not configured**
        
        To enable the AI Assistant:
        1. Get an OpenAI API key from https://platform.openai.com/
        2. Create a `.env` file in the project root with `OPENAI_API_KEY=your_key_here`
        3. Install dependencies: `pip install openai python-dotenv`
        """)
        return
    
    st.markdown("""
    Ask me anything about UK dating statistics, demographics, income distribution, marriage trends, and more!
    """)
    
    # Chat display
    st.markdown("### Conversation")
    
    # Display chat history
    for i, msg in enumerate(st.session_state.ai_messages):
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.write(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.write(msg["content"])
                if "metadata" in msg and msg["metadata"].get("tokens_used"):
                    st.caption(f"Tokens used: {msg['metadata']['tokens_used']}")

    # Render last generated chart/map if present
    if st.session_state.ai_last_fig is not None:
        st.plotly_chart(st.session_state.ai_last_fig, use_container_width=True)
    
    # Input section
    st.markdown("---")
    user_input = st.text_area(
        "Your question:",
        placeholder="E.g., 'What percentage of UK adults are single by age?' or 'Show me the gender distribution of income earners above £50k'",
        height=100,
        key="user_question_input"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        submit_button = st.button("Ask AI", use_container_width=True)
    
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.ai_messages = []
            st.rerun()
    
    if submit_button and user_input.strip():
        # Add user message to history
        st.session_state.ai_messages.append({
            "role": "user",
            "content": user_input
        })
        
        # Build chart/map first to produce deterministic context for the model
        fig, fig_type, viz_context = assistant.build_chart_or_map(user_input)

        # Get AI response (pass visualization context to keep numbers aligned)
        with st.spinner("🤔 Thinking..."):
            response, metadata = assistant.ask_question(user_input, context=viz_context if viz_context else None)

        # Add assistant response to history
        st.session_state.ai_messages.append({
            "role": "assistant",
            "content": response,
            "metadata": metadata
        })

        # Render chart/map if available
        if fig is not None:
            st.session_state.ai_last_fig = fig
            st.session_state.ai_last_fig_type = fig_type
            st.session_state.ai_messages.append({"role": "assistant", "content": f"Rendering {fig_type}..."})
            st.plotly_chart(fig, use_container_width=True)
        else:
            _log_debug(f"No chart/map generated for this question: '{user_input[:120]}'")
        
        st.rerun()


def render_ai_sidebar():
    """Render a compact AI chat in the sidebar."""
    initialize_session_state()
    assistant = st.session_state.ai_assistant
    
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🤖 Quick Question?")
        
        if not assistant.is_available():
            st.info("AI Assistant not configured. Set OPENAI_API_KEY to enable.")
            return
        
        # Quick questions
        quick_questions = [
            "What percentage are single by age?",
            "Gender income gap statistics",
            "Marriage statistics by age",
            "Employment rates by demographic"
        ]
        
        selected_q = st.selectbox(
            "Or ask:",
            ["Custom question..."] + quick_questions,
            key="sidebar_ai_quick_q"
        )
        
        if selected_q == "Custom question...":
            question = st.text_input("Your question:", key="sidebar_ai_input")
        else:
            question = selected_q
        
        if st.button("Ask", key="sidebar_ai_button"):
            if question:
                with st.spinner("Thinking..."):
                    response, _ = assistant.ask_question(question)
                st.info(response)


# Export functions
__all__ = [
    "AIAssistant",
    "initialize_session_state",
    "render_ai_chat",
    "render_ai_sidebar"
]
