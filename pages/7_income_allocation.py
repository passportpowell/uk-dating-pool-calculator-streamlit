import streamlit as st
import pandas as pd
import os
from openai import OpenAI
from src.utils.styles import CUSTOM_CSS

st.set_page_config(
    page_title="Income Allocation Planner - UK Dating Statistics",
    page_icon="💷",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown('<div class="main-header">💷 Income Allocation Planner</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analyze your household income and see a clear split across essentials, kids, savings, and lifestyle</div>', unsafe_allow_html=True)

# Car costs (annual, 2025-2026 estimates) - EXCLUDING depreciation
# Sources: AA Motoring Costs (2025), RAC Report (2024), Nimblefins (2025)
# Based on 6,000 miles per year per car (UK median for non-driving jobs)
CAR_COSTS = {
    "small_car": {
        "insurance": 450,  # UK median comprehensive
        "fuel": 600,  # 6,000 miles @ 50mpg, £1.45/litre
        "tax": 190,  # VED Band B-C
        "mot_service": 250,  # MOT £55 + service £200
        "repairs": 300,  # Average annual repairs/tyres
    },
    "medium_car": {
        "insurance": 550,
        "fuel": 800,  # 6,000 miles @ 40mpg
        "tax": 190,
        "mot_service": 300,
        "repairs": 400,
    },
    "large_car": {
        "insurance": 700,
        "fuel": 1100,  # 6,000 miles @ 32mpg
        "tax": 190,
        "mot_service": 350,
        "repairs": 500,
    },
    "electric": {
        "insurance": 600,
        "fuel": 200,  # Electricity for 6,000 miles
        "tax": 0,  # Currently exempt
        "mot_service": 200,  # Lower service costs
        "repairs": 250,
    }
}

# Create tabs for manual entry vs CSV upload
tab_manual, tab_csv = st.tabs(["📝 Manual Entry", "📊 Upload & Analyze CSV"])

# Initialize OpenAI client
openai_key = os.getenv("OPENAI_API_KEY")
if openai_key:
    client = OpenAI(api_key=openai_key)
else:
    client = None

# ============ AI ANALYSIS FUNCTION ============
@st.cache_data(show_spinner=False)
def analyze_budget_with_ai(budget_dict_str, net_income):
    """Use AI to analyze budget and recommend allocation"""
    if not client:
        return None
    
    prompt = f"""Analyze this UK household budget and provide specific, actionable recommendations.

Monthly Budget:
{budget_dict_str}

Annual Net Income: £{net_income:,.0f}
Monthly Net Income: £{net_income/12:,.0f}

Please provide:
1. Quick assessment of spending patterns (1-2 sentences)
2. Three specific recommendations to optimize allocation
3. Suggested percentage split for Essential/Children/Savings/Lifestyle
4. Any red flags or concerns

Keep responses concise and practical."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=400
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"

@st.cache_data(show_spinner=False)
def analyze_recommended_allocation_with_ai(rec_monthly_str, csv_net_income, fixed_essentials_monthly, parsed_budget_str):
    """Use AI to analyze the final recommended allocation and provide insights"""
    if not client:
        return None
    
    net_monthly = csv_net_income / 12
    
    prompt = f"""You are a UK financial advisor. Analyze this person's recommended allocation and compare it to their actual budget.

INCOME & ESSENTIAL COSTS:
- Monthly net income: £{net_monthly:,.2f}
- Fixed essentials: £{fixed_essentials_monthly:,.2f}/month

YOUR ACTUAL CURRENT BUDGET:
{parsed_budget_str}

RECOMMENDED ALLOCATION (from strategy):
{rec_monthly_str}

ANALYSIS NEEDED:
1. Is this recommended allocation realistic and sustainable for them?
2. How does their actual spending compare to the recommendation? Where are the biggest gaps?
3. What are the top 2-3 priorities they should focus on?
4. Any red flags or concerns about their financial health?
5. Specific, actionable steps they can take in the next month to move toward this allocation?

Be encouraging but honest. Focus on practical changes, not judgment. If they're doing well in any area, acknowledge it."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis unavailable: {str(e)}"

@st.cache_data(show_spinner=False)
def analyze_goals_feasibility_with_ai(goals_str, available_savings, csv_net_income, fixed_essentials_monthly):
    """Use AI to analyze if life goals are feasible and suggest adjustments"""
    if not client:
        return None
    
    net_monthly = csv_net_income / 12
    
    prompt = f"""You are a UK financial advisor. Analyze this person's life goals and budget allocation.

INCOME & FIXED COSTS:
- Monthly net income: £{net_monthly:,.2f}
- Fixed essentials (rent, tax, utilities, phone): £{fixed_essentials_monthly:,.2f}/month

LIFE GOALS (Monthly savings needed):
{goals_str}

ALLOCATED SAVINGS BUDGET:
Available for savings (from strategy): £{available_savings:,.2f}/month

ANALYSIS:
1. Are these goals feasible within the allocated savings budget?
2. If goals exceed savings budget, what would you recommend reducing or adjusting?
3. What's the realistic timeline for achieving these goals?
4. Any other financial considerations they should be aware of?

Provide practical, actionable advice. Be encouraging but honest about constraints."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Analysis unavailable: {str(e)}"



@st.cache_data(show_spinner=False)
def validate_and_fix_budget_with_ai(df_preview_str, detected_budget_str, detected_income):
    """Use AI to validate parsing and detect anomalies like double-counting"""
    if not client:
        return None
    
    prompt = f"""You are a UK budget expert. I've parsed a CSV budget file and need your help validate it.

Detected Monthly Budget:
{detected_budget_str}

First 10 rows of raw CSV:
{df_preview_str}

IMPORTANT CHECKS:
1. Does this budget look realistic? If spend > income, it's likely DOUBLE COUNTING.
2. Are there "Total" rows being counted twice?
3. Are there account names being miscategorized?
4. Does the total spend seem reasonable compared to income?

If you detect issues, list them clearly with ISSUE/FIX/REASON.
If budget looks correct, just say "Budget looks reasonable - no major issues detected."
Be concise."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Validation unavailable: {str(e)}"

# ============ AI CHAT FUNCTIONS ============
def initialize_allocation_chat_state():
    """Initialize chat history for allocation questions."""
    if "allocation_chat_messages" not in st.session_state:
        st.session_state.allocation_chat_messages = []
    if "allocation_chat_context" not in st.session_state:
        st.session_state.allocation_chat_context = ""


def render_allocation_ai_chat(context_summary=""):
    """Render AI chat interface for asking questions about the allocation."""
    initialize_allocation_chat_state()
    
    if not client:
        st.warning("⚠️ AI chat is not configured. Please set OPENAI_API_KEY to enable.")
        return
    
    with st.expander("🤖 Ask Questions About Your Allocation", expanded=True):
        st.markdown("Ask me anything about your recommended allocation, spending patterns, or strategies to achieve your financial goals.")
        
        # Update context if provided
        if context_summary:
            st.session_state.allocation_chat_context = context_summary
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for msg in st.session_state.allocation_chat_messages:
                if msg["role"] == "user":
                    with st.chat_message("user"):
                        st.write(msg["content"])
                else:
                    with st.chat_message("assistant"):
                        st.write(msg["content"])
        
        # Input section
        col1, col2 = st.columns([4, 1])
        
        with col1:
            user_question = st.text_input(
                "Ask a question about your allocation:",
                placeholder="E.g., 'How can I reduce my essential expenses?' or 'Is my savings target realistic?'",
                key="allocation_chat_input"
            )
        
        with col2:
            if st.button("Send", use_container_width=True, key="allocation_chat_send"):
                if user_question.strip():
                    # Add user message
                    st.session_state.allocation_chat_messages.append({
                        "role": "user",
                        "content": user_question
                    })
                    
                    # Build context for AI
                    context_msg = ""
                    if st.session_state.allocation_chat_context:
                        context_msg = f"User's financial context:\n{st.session_state.allocation_chat_context}\n\n"
                    
                    # Prepare messages for AI
                    system_prompt = """You are a knowledgeable UK financial advisor specializing in income allocation and budgeting.

Your role is to:
1. Provide personalized advice about the user's recommended allocation
2. Help them understand how to adjust their spending
3. Suggest practical strategies to achieve savings and lifestyle goals
4. Address concerns about financial feasibility
5. Encourage realistic and sustainable financial practices

When responding:
- Be specific and practical, not theoretical
- Reference their actual numbers when mentioned in context
- Provide actionable steps they can take
- Be encouraging but honest about constraints
- Focus on their "Your Recommended Monthly Allocation" and "Allocation Analysis & Next Steps"
- Suggest how they can move from their current spending toward the recommended allocation"""
                    
                    messages = [
                        {"role": "system", "content": system_prompt}
                    ]
                    
                    # Add context if available
                    if context_msg:
                        messages.append({
                            "role": "user",
                            "content": f"{context_msg}Based on this context, please answer the following question."
                        })
                        messages.append({
                            "role": "assistant",
                            "content": "I understand your financial situation. I'm ready to help with your question."
                        })
                    
                    # Add conversation history (last 10 messages to keep context manageable)
                    for msg in st.session_state.allocation_chat_messages[-10:]:
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                    
                    # Get AI response
                    with st.spinner("💭 Thinking..."):
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4o-mini",
                                messages=messages,
                                temperature=0.7,
                                max_tokens=600
                            )
                            ai_response = response.choices[0].message.content
                        except Exception as e:
                            ai_response = f"Sorry, I encountered an error: {str(e)}"
                    
                    # Add assistant response
                    st.session_state.allocation_chat_messages.append({
                        "role": "assistant",
                        "content": ai_response
                    })
                    
                    st.rerun()
        
        # Clear chat button
        if st.button("Clear Chat History", key="allocation_chat_clear"):
            st.session_state.allocation_chat_messages = []
            st.rerun()

# ============ PARSING FUNCTION ============
def parse_budget_csv(uploaded_file):
    try:
        # Try reading with different approaches
        df = None
        errors = []
        
        # Attempt 1: standard read
        try:
            df = pd.read_csv(uploaded_file, skip_blank_lines=True)
        except Exception as e:
            errors.append(f"Standard read failed: {str(e)}")
        
        # Attempt 2: read without header if first attempt fails or has "Unnamed"
        if df is None or any("Unnamed" in str(col) for col in df.columns):
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, header=None, skip_blank_lines=True)
                if len(df) > 0:
                    df.columns = [f"col_{i}" for i in range(len(df.columns))]
            except Exception as e:
                errors.append(f"No-header read failed: {str(e)}")
        
        # Attempt 3: read with different separators (semicolon, tab)
        if df is None or len(df) == 0:
            try:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, sep=None, engine='python', skip_blank_lines=True)
            except Exception as e:
                errors.append(f"Auto-separator read failed: {str(e)}")
        
        if df is None or len(df) == 0:
            st.error(f"Could not read the CSV file. It may be empty or in an unsupported format.\nDetails: {'; '.join(errors)}")
            return None
            
    except Exception as e:
        st.error(f"File read error: {str(e)}")
        return None

    # Try to find a text/category column and a numeric/amount column
    text_cols = []
    numeric_cols = []
    
    # Show sample of data for debugging
    st.write("**CSV Data Preview:**")
    df_display = df.head(60).fillna(0)
    st.dataframe(df_display, use_container_width=True)
    
    for col in df.columns:
        try:
            # Try to convert to numeric, stripping currency symbols and commas
            col_clean = df[col].astype(str).str.replace('€', '').str.replace('£', '').str.replace('$', '').str.replace(',', '').str.strip()
            numeric_test = pd.to_numeric(col_clean, errors="coerce")
            non_null_count = numeric_test.notna().sum()
            if non_null_count > 0:
                numeric_cols.append((col, non_null_count))
        except:
            pass
        
        # Check if it's mostly text (non-numeric)
        if df[col].dtype == 'object':
            col_clean = df[col].astype(str).str.replace('€', '').str.replace('£', '').str.replace('$', '').str.replace(',', '').str.strip()
            numeric_test = pd.to_numeric(col_clean, errors="coerce")
            if numeric_test.isna().sum() > numeric_test.notna().sum():
                # More NaNs than numbers = likely text column
                text_cols.append(col)
    
    # Sort numeric cols by count of valid numbers (most numbers first)
    numeric_cols.sort(key=lambda x: x[1], reverse=True)
    
    # Prefer column with "amount" in the name, otherwise pick the one with most values
    amount_col = None
    for col, count in numeric_cols:
        if "amount" in str(col).lower():
            amount_col = col
            break
    
    if not amount_col and numeric_cols:
        amount_col = numeric_cols[0][0]
    
    # Use first text column as bucket, selected numeric column as amount
    bucket_col = text_cols[0] if text_cols else None
    
    if not bucket_col:
        st.error(f"❌ Could not find a text column for budget items.\nColumns found: {list(df.columns)}\n\nPlease ensure your CSV has at least one text column with item names.")
        return None
    
    if not amount_col:
        st.error(f"❌ Could not find a numeric column for amounts.\nColumns found: {list(df.columns)}\nColumn types: {dict(df.dtypes)}\n\nPlease check that amounts are numeric (numbers, not text with symbols).")
        return None
    
    st.success(f"✅ Detected: Items in '{bucket_col}', Amounts in '{amount_col}'")

    bucket_keywords = {
        "Essential": ["rent", "housing", "bills", "utilities", "transport", "commute", "essential", "groceries", "food", "phone", "internet", "insurance", "tax", "mortgage", "council", "gas", "electric", "water"],
        "Children": ["child", "kids", "education", "childcare", "activities", "school"],
        "Savings": ["savings", "invest", "pension", "bond", "fund"],
        "Lifestyle": ["lifestyle", "fun", "holiday", "travel", "leisure", "entertainment", "hobby"],
    }
    
    # Fixed essential items that cannot be changed
    fixed_essential_keywords = [
        "rent", "mortgage", "tax", "council tax", "mobile phone", "phone",
        "electric", "gas", "water", "utilities", "revolut business"
    ]

    totals = {"Essential": 0.0, "Children": 0.0, "Savings": 0.0, "Lifestyle": 0.0}
    fixed_essentials = 0.0
    flexible_spending = {"Essential": 0.0, "Children": 0.0, "Savings": 0.0, "Lifestyle": 0.0}
    detected_monthly_income = None
    included_rows = []
    skipped_rows = []
    
    for _, row in df.iterrows():
        raw_bucket = str(row[bucket_col]).strip().lower()
        
        # Skip header rows, metadata, empty rows, and summary sections
        skip_keywords = [
            "description", "item", "category", "expense", "amount", "none", "live in uk",
            "total", "monzo", "revolut", "account", "business", "remaining", "balance", 
            "rp", "rb", "subscription"
        ]
        
        if not raw_bucket or any(kw in raw_bucket for kw in skip_keywords):
            skipped_rows.append({
                "item": str(row[bucket_col]),
                "reason": "header/summary/account",
                "raw": raw_bucket
            })
            continue
        
        # Remove leading dashes or bullets
        raw_bucket = raw_bucket.lstrip('-').lstrip('•').lstrip('*').strip()
        
        # Check for income row
        if "income" in raw_bucket or "salary" in raw_bucket or "earnings" in raw_bucket:
            try:
                amount_str = str(row[amount_col]).replace('€', '').replace('£', '').replace('$', '').replace(',', '').strip()
                detected_monthly_income = pd.to_numeric(amount_str, errors="coerce")
                if detected_monthly_income and not pd.isna(detected_monthly_income):
                    detected_monthly_income = float(detected_monthly_income)
            except:
                pass
            continue
        
        # Categorize using keyword matching
        target = "Lifestyle"  # default
        for bucket_name, keywords in bucket_keywords.items():
            if any(keyword in raw_bucket for keyword in keywords):
                target = bucket_name
                break

        monthly_value = None
        try:
            # Clean amount: strip currency symbols and commas
            amount_str = str(row[amount_col]).replace('€', '').replace('£', '').replace('$', '').replace(',', '').strip()
            monthly_value = pd.to_numeric(amount_str, errors="coerce")
        except:
            monthly_value = None
        
        if monthly_value is None or pd.isna(monthly_value):
            monthly_value = 0
        
        amount_val = float(monthly_value if monthly_value else 0)
        totals[target] += amount_val
        
        # Check if this is a fixed essential
        is_fixed = any(kw in raw_bucket for kw in fixed_essential_keywords)
        if is_fixed and target == "Essential":
            fixed_essentials += amount_val
        else:
            flexible_spending[target] += amount_val
        
        included_rows.append({
            "item": str(row[bucket_col]).strip(),
            "bucket": target,
            "monthly": amount_val,
            "fixed": "🔒 Fixed" if is_fixed else "✏️ Flexible"
        })

    # Separate fixed essentials by item for granular display
    fixed_essential_items = [r for r in included_rows if r["fixed"] == "🔒 Fixed"]
    
    # Check if CSV has savings data
    has_savings_data = totals.get("Savings", 0) > 0
    
    # Return totals, detected income, preview, row details, and fixed/flexible breakdown
    return totals, detected_monthly_income, df.head(60).fillna(0), included_rows, skipped_rows, fixed_essentials, flexible_spending, fixed_essential_items, has_savings_data

# ============ MANUAL ENTRY TAB ============
with tab_manual:
    st.sidebar.header("📝 Manual Entry - Income Inputs")
    gross_income = st.sidebar.number_input(
        "Annual household gross income (£)",
        min_value=0,
        max_value=5_000_000,
        value=75_000,
        step=1_000,
    )

    take_home_pct = st.sidebar.slider(
        "Take-home (net) % of gross",
        min_value=50,
        max_value=90,
        value=70,
        help="Approximate how much of gross income you keep after tax/pension. Typical range is 60-75%.",
    )

    profiles = {
        "Balanced 50/20/20/10": {"Essential": 0.50, "Children": 0.20, "Savings": 0.20, "Lifestyle": 0.10},
        "High Savings 45/15/30/10": {"Essential": 0.45, "Children": 0.15, "Savings": 0.30, "Lifestyle": 0.10},
        "Family Heavy 45/30/15/10": {"Essential": 0.45, "Children": 0.30, "Savings": 0.15, "Lifestyle": 0.10},
        "Lower Fixed Costs 40/20/25/15": {"Essential": 0.40, "Children": 0.20, "Savings": 0.25, "Lifestyle": 0.15},
    }

    profile_name = st.sidebar.selectbox("Guideline split", list(profiles.keys()))
    guideline = profiles[profile_name]

    if st.sidebar.checkbox("Customise split", value=False):
        essential_pct = st.sidebar.slider("Essential (%)", 0, 100, int(guideline["Essential"] * 100))
        children_pct = st.sidebar.slider("Children (%)", 0, 100, int(guideline["Children"] * 100))
        savings_pct = st.sidebar.slider("Savings (%)", 0, 100, int(guideline["Savings"] * 100))
        lifestyle_pct = st.sidebar.slider("Lifestyle (%)", 0, 100, int(guideline["Lifestyle"] * 100))
        total_pct = essential_pct + children_pct + savings_pct + lifestyle_pct
        normaliser = total_pct if total_pct > 0 else 100
        guideline = {
            "Essential": essential_pct / normaliser,
            "Children": children_pct / normaliser,
            "Savings": savings_pct / normaliser,
            "Lifestyle": lifestyle_pct / normaliser,
        }
        st.sidebar.caption(f"Normalised to 100% (you entered {total_pct}%)")

    st.sidebar.header("Transportation")
    num_cars = st.sidebar.number_input("Number of cars in household", min_value=0, max_value=5, value=0)
    car_costs_monthly = 0
    car_breakdown = {}
    if num_cars > 0:
        car_type = st.sidebar.selectbox(
            "Car type",
            ["Small car", "Medium car", "Large/SUV", "Electric"]
        )
        car_key = car_type.lower().replace("/", "").replace(" ", "_")
        if car_type == "Small car":
            car_key = "small_car"
        elif car_type == "Medium car":
            car_key = "medium_car"
        elif car_type == "Large/SUV":
            car_key = "large_car"
        
        if car_key in CAR_COSTS:
            annual_car_cost = sum(CAR_COSTS[car_key].values())
            car_costs_monthly = (annual_car_cost * num_cars) / 12
            car_breakdown = {item: (cost * num_cars) / 12 for item, cost in CAR_COSTS[car_key].items()}
            st.sidebar.info(f"📊 Monthly car cost: £{car_costs_monthly:,.0f} ({num_cars} × {car_type})")
    
    st.sidebar.header("Your planned spend (per month)")
    planned_monthly = {
        "Essential": st.sidebar.number_input("Essential (housing, bills, food)", min_value=0, max_value=1_000_000, value=0, step=50),
        "Children": st.sidebar.number_input("Children (education, childcare, activities)", min_value=0, max_value=1_000_000, value=0, step=50),
        "Savings": st.sidebar.number_input("Savings & investing", min_value=0, max_value=1_000_000, value=0, step=50),
        "Lifestyle": st.sidebar.number_input("Lifestyle (holidays, entertainment)", min_value=0, max_value=1_000_000, value=0, step=50),
    }
    
    # Add car costs to Essential bucket
    planned_monthly["Essential"] += car_costs_monthly

    net_income = gross_income * (take_home_pct / 100)
    net_monthly = net_income / 12
    planned_annual_total = sum(v * 12 for v in planned_monthly.values())
    surplus = net_income - planned_annual_total

    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Net income (annual)", f"£{net_income:,.0f}")
    with col2:
        st.metric("Net income (monthly)", f"£{net_monthly:,.0f}")
    with col3:
        st.metric("Planned spend (annual)", f"£{planned_annual_total:,.0f}")
    with col4:
        st.metric("Surplus / shortfall", f"£{surplus:,.0f}")

    # Build suggested rows
    suggested_rows = []
    for bucket, pct in guideline.items():
        suggested_annual = net_income * pct
        planned_annual = planned_monthly[bucket] * 12
        delta = planned_annual - suggested_annual
        suggested_rows.append(
            {
                "Bucket": bucket,
                "Guideline %": f"{pct * 100:.0f}%",
                "Suggested annual": suggested_annual,
                "Suggested monthly": suggested_annual / 12,
                "Planned annual": planned_annual,
                "Planned monthly": planned_monthly[bucket],
                "Planned % of net": f"{(planned_annual / net_income * 100) if net_income else 0:.1f}%",
                "Over / under": delta,
            }
        )

    # Quick insights
    if net_income > 0:
        planned_pct_of_net = planned_annual_total / net_income
        savings_rate = (planned_monthly["Savings"] * 12) / net_income
        top_over = max(suggested_rows, key=lambda x: x["Over / under"]) if suggested_rows else None
        top_under = min(suggested_rows, key=lambda x: x["Over / under"]) if suggested_rows else None

        insight_col1, insight_col2, insight_col3 = st.columns(3)
        with insight_col1:
            st.info(f"Planned spend is {(planned_pct_of_net * 100):.1f}% of net income — {('over' if surplus < 0 else 'under')} by £{abs(surplus):,.0f}/yr.")
        with insight_col2:
            st.info(f"Savings rate from your plan: {(savings_rate * 100):.1f}% of net vs guideline {guideline['Savings'] * 100:.0f}%.")
        with insight_col3:
            if top_over and top_under:
                st.info(f"Biggest over vs guideline: {top_over['Bucket']} (by £{top_over['Over / under']:,.0f}); biggest under: {top_under['Bucket']}.")
            else:
                st.info("Adjust inputs to see over/under by bucket.")

    alloc_df = pd.DataFrame(suggested_rows)

    if not alloc_df.empty:
        formatted_df = alloc_df.copy()
        formatted_df["Suggested annual"] = formatted_df["Suggested annual"].apply(lambda x: f"£{x:,.0f}")
        formatted_df["Suggested monthly"] = formatted_df["Suggested monthly"].apply(lambda x: f"£{x:,.0f}")
        formatted_df["Planned annual"] = formatted_df["Planned annual"].apply(lambda x: f"£{x:,.0f}")
        formatted_df["Planned monthly"] = formatted_df["Planned monthly"].apply(lambda x: f"£{x:,.0f}")
        formatted_df["Over / under"] = formatted_df["Over / under"].apply(lambda x: f"£{x:,.0f}")

        st.subheader("Suggested split vs. your plan")
        st.dataframe(formatted_df, hide_index=True, use_container_width=True)

        chart_data = alloc_df[["Bucket", "Suggested annual", "Planned annual"]].set_index("Bucket")
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            st.bar_chart(chart_data, height=320)
        with chart_col2:
            st.line_chart(chart_data, height=320)

        # Recommended split
        recommended = guideline.copy()
        recommended["Savings"] = max(recommended.get("Savings", 0), 0.15)
        recommended["Lifestyle"] = min(recommended.get("Lifestyle", 0.1), 0.15)
        recommended["Essential"] = min(recommended.get("Essential", 0.5), 0.55)
        total_rec = sum(recommended.values())
        recommended = {k: v / total_rec for k, v in recommended.items()}

        rec_rows = []
        for bucket, pct in recommended.items():
            rec_rows.append(
                {
                    "Bucket": bucket,
                    "Recommended %": f"{pct * 100:.0f}%",
                    "Recommended annual": net_income * pct,
                    "Recommended monthly": (net_income * pct) / 12,
                }
            )
        rec_df = pd.DataFrame(rec_rows)
        rec_df["Recommended annual"] = rec_df["Recommended annual"].apply(lambda x: f"£{x:,.0f}")
        rec_df["Recommended monthly"] = rec_df["Recommended monthly"].apply(lambda x: f"£{x:,.0f}")

        st.subheader("Recommended split (guardrails applied)")
        st.dataframe(rec_df, hide_index=True, use_container_width=True)
    else:
        st.info("Enter your income and planned spend to see suggestions.")

    st.markdown("---")
    st.markdown("""
    **Manual Entry Guide**
    - Set your gross income and take-home %.
    - Pick a guideline split or customise it to match your priorities.
    - Enter planned monthly spend per bucket.
    - Charts show suggested vs planned allocations; adjust to balance surplus/shortfall.
    """)

# ============ CSV UPLOAD & ANALYSIS TAB ============
with tab_csv:
    st.header("📊 Upload & Analyze Budget CSV")
    st.markdown("Upload your budget CSV and we'll categorize it, analyze spending patterns, and show AI-powered recommendations.")

    uploaded_file = st.file_uploader(
        "Choose a CSV file with your budget",
        type=["csv"],
        help="Columns needed: bucket/category and monthly/annual amount"
    )

    if uploaded_file:
        parsed_result = parse_budget_csv(uploaded_file)
        
        if parsed_result:
            parsed, detected_monthly_income, df_preview, included_rows, skipped_rows, fixed_essentials, flexible_spending, fixed_essential_items, has_savings_data = parsed_result
            st.success("✅ Budget loaded and categorized!")
            
            # Show fixed vs flexible breakdown
            st.info(f"🔒 **Fixed essentials:** £{fixed_essentials:,.0f}/month • ✏️ **Flexible spending:** £{sum(flexible_spending.values()):,.0f}/month")
            
            # Optional AI Validation - only if user enables it
            show_ai_validation = st.checkbox("✅ Validate budget with AI (checks for double-counting)", value=False, key="show_ai_validation")
            if show_ai_validation:
                with st.spinner("🤖 Validating budget data..."):
                    budget_summary = "\n".join([f"{bucket}: £{amount:,.0f}/month" for bucket, amount in parsed.items()])
                    df_preview_str = df_preview.head(10).to_string()
                    validation_message = validate_and_fix_budget_with_ai(df_preview_str, budget_summary, detected_monthly_income)
                
                if validation_message and "issue" in validation_message.lower():
                    st.warning("⚠️ **Potential Issues Detected:**\n" + validation_message)
                elif validation_message:
                    st.info("✅ **Validation:** " + validation_message)
            
            # CSV-only mode: use income exactly as given in the CSV (monthly → annual)
            default_net = int(detected_monthly_income * 12) if detected_monthly_income else 0
            csv_net_income = st.number_input(
                "Annual household net income (£) — from CSV",
                min_value=0,
                max_value=5_000_000,
                value=default_net,
                step=500,
                help="This uses the monthly income detected in your CSV (×12). No derived gross or take-home is applied.",
                key="csv_net_income",
            )

            csv_planned_annual = sum(parsed.values()) * 12
            csv_surplus = csv_net_income - csv_planned_annual
            
            # AI Analysis - Only call if user enables it (lazy loading)
            show_ai_budget_analysis = st.checkbox("💭 Show AI budget analysis", value=False, key="show_ai_budget_analysis")
            if show_ai_budget_analysis:
                with st.spinner("🤖 Analyzing your budget with AI..."):
                    budget_summary = "\n".join([
                        f"{bucket}: £{amount:,.0f}/month (£{amount*12:,.0f}/year)"
                        for bucket, amount in parsed.items()
                    ])
                    ai_analysis = analyze_budget_with_ai(budget_summary, csv_net_income)
                
                if ai_analysis:
                    st.markdown("### 🤖 AI Budget Analysis")
                    st.markdown(ai_analysis)
                st.markdown("---")
            
            # Metrics (CSV-only, no derived figures)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Net income (CSV)", f"£{csv_net_income:,.0f}")
            with col2:
                st.metric("Uploaded spend (annual)", f"£{csv_planned_annual:,.0f}")
            with col3:
                st.metric("Surplus / shortfall", f"£{csv_surplus:,.0f}")
            
            st.markdown("---")
            
            # Show parsed budget
            st.subheader("📂 Your Budget (mapped to buckets)")
            budget_df = pd.DataFrame([
                {"Bucket": k, "Monthly": f"£{v:,.0f}", "Annual": f"£{v*12:,.0f}"} 
                for k, v in parsed.items()
            ])
            st.dataframe(budget_df, hide_index=True, use_container_width=True)
            
            # Debug: Show total monthly budget
            total_monthly = sum(parsed.values())
            with st.expander("🔍 Debug: Monthly totals by bucket"):
                for bucket, amount in parsed.items():
                    st.write(f"{bucket}: £{amount:,.2f}/month")

            # Rows actually counted in totals
            with st.expander("🧾 Rows included in totals"):
                if included_rows:
                    inc_df = pd.DataFrame(included_rows)
                    inc_df_sorted = inc_df.sort_values(by=["bucket","item"]).copy()
                    inc_df_sorted["monthly"] = inc_df_sorted["monthly"].apply(lambda x: f"£{x:,.2f}")
                    st.dataframe(inc_df_sorted, hide_index=True, use_container_width=True)
                    st.caption(f"Counted rows: {len(inc_df)} • Monthly sum: £{total_monthly:,.2f}")
                else:
                    st.info("No counted rows found.")

            # Rows skipped (headers, totals, accounts)
            with st.expander("🚫 Rows skipped (summary/account/header)"):
                if skipped_rows:
                    skip_df = pd.DataFrame(skipped_rows)
                    st.dataframe(skip_df, hide_index=True, use_container_width=True)
                    st.caption(f"Skipped rows: {len(skip_df)}")
                else:
                    st.info("No skipped rows.")
            
            st.markdown("---")
            
            # AI Insights
            st.subheader("🤖 Analysis & Recommendations")
            csv_savings_rate = (parsed.get("Savings", 0) * 12 / csv_net_income) if csv_net_income else 0
            csv_essential_rate = (parsed.get("Essential", 0) * 12 / csv_net_income) if csv_net_income else 0
            
            insight1, insight2, insight3 = st.columns(3)
            with insight1:
                status = "✅" if csv_savings_rate >= 0.15 else "⚠️"
                st.info(f"{status} Savings rate: {csv_savings_rate*100:.1f}%\n(target: 15%+)")
            with insight2:
                status = "✅" if csv_essential_rate <= 0.55 else "⚠️"
                st.info(f"{status} Essential ratio: {csv_essential_rate*100:.1f}%\n(target: ≤55%)")
            with insight3:
                status = "✅" if csv_surplus >= 0 else "⚠️"
                st.info(f"{status} Surplus/shortfall:\n£{csv_surplus:,.0f}/yr")
            
            st.markdown("---")
            
            # Recommended guidelines
            st.subheader("📊 Budget vs Recommended Split")
            guideline_options = {
                "Balanced 50/20/20/10": {"Essential": 0.50, "Children": 0.20, "Savings": 0.20, "Lifestyle": 0.10},
                "High Savings 45/15/30/10": {"Essential": 0.45, "Children": 0.15, "Savings": 0.30, "Lifestyle": 0.10},
                "Family Heavy 45/30/15/10": {"Essential": 0.45, "Children": 0.30, "Savings": 0.15, "Lifestyle": 0.10},
                "Conservative 40/20/25/15": {"Essential": 0.40, "Children": 0.20, "Savings": 0.25, "Lifestyle": 0.15},
            }
            
            selected_profile = st.selectbox("Choose a recommended split profile", list(guideline_options.keys()), key="csv_profile")
            rec_guideline = guideline_options[selected_profile]
            
            rec_data = []
            for bucket, pct in rec_guideline.items():
                rec_annual = csv_net_income * pct
                actual_annual = parsed.get(bucket, 0) * 12
                delta = actual_annual - rec_annual
                rec_data.append({
                    "Bucket": bucket,
                    "Recommended %": f"{pct*100:.0f}%",
                    "Recommended annual": f"£{rec_annual:,.0f}",
                    "Your actual": f"£{actual_annual:,.0f}",
                    "Difference": f"£{delta:,.0f}" if delta >= 0 else f"-£{abs(delta):,.0f}",
                })
            
            rec_comp_df = pd.DataFrame(rec_data)
            st.dataframe(rec_comp_df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # LIFE GOALS SECTION - Before allocation strategies
            with st.expander("🎯 Life Goals & Savings Targets", expanded=True):
                st.markdown("Set your financial goals to calculate how much you need to save monthly.")
                
                goals_col1, goals_col2, goals_col3, goals_col4 = st.columns(4)
                with goals_col1:
                    num_children = st.number_input(
                        "Number of children (or planning)",
                        min_value=0,
                        max_value=10,
                        value=0,
                        key="num_children"
                    )
                with goals_col2:
                    buying_house = st.checkbox("Planning to buy a house", key="buying_house")
                    if buying_house:
                        house_years = st.slider(
                            "Timeline (years)",
                            min_value=1,
                            max_value=20,
                            value=5,
                            key="house_years"
                        )
                        house_price = st.number_input(
                            "Target house price (£)",
                            min_value=50000,
                            max_value=2000000,
                            value=400000,
                            step=10000,
                            key="house_price"
                        )
                        deposit_pct = st.slider(
                            "Deposit %",
                            min_value=5,
                            max_value=40,
                            value=20,
                            key="deposit_pct"
                        )
                    else:
                        house_years = house_price = deposit_pct = 0
                
                with goals_col3:
                    buying_car = st.checkbox("Planning to buy a car", key="buying_car")
                    car_type_selected = None
                    car_running_costs_monthly = 0
                    if buying_car:
                        car_type_selected = st.selectbox(
                            "Car type",
                            ["Small car", "Medium car", "Large/SUV", "Electric"],
                            key="car_type_goal"
                        )
                        
                        # Get car costs for this type
                        car_key = "small_car"
                        if car_type_selected == "Small car":
                            car_key = "small_car"
                        elif car_type_selected == "Medium car":
                            car_key = "medium_car"
                        elif car_type_selected == "Large/SUV":
                            car_key = "large_car"
                        elif car_type_selected == "Electric":
                            car_key = "electric"
                        
                        if car_key in CAR_COSTS:
                            annual_cost = sum(CAR_COSTS[car_key].values())
                            car_running_costs_monthly = annual_cost / 12
                            
                            # Show breakdown
                            st.markdown(f"**📊 {car_type_selected} Running Costs (Annual)**")
                            cost_breakdown = CAR_COSTS[car_key]
                            for item, cost in cost_breakdown.items():
                                st.caption(f"  {item.title()}: £{cost:,.0f}")
                            st.info(f"💷 Monthly running cost: £{car_running_costs_monthly:,.0f}/month (£{annual_cost:,.0f}/year)")
                        
                        car_years = st.slider(
                            "Timeline to buy (years)",
                            min_value=1,
                            max_value=10,
                            value=2,
                            key="car_years"
                        )
                        car_price = st.number_input(
                            "Target car price (£)",
                            min_value=5000,
                            max_value=150000,
                            value=20000,
                            step=1000,
                            key="car_price"
                        )
                    else:
                        car_years = car_price = 0
                
                with goals_col4:
                    emergency_fund_months = st.slider(
                        "Emergency fund (months of expenses)",
                        min_value=1,
                        max_value=12,
                        value=3,
                        key="emergency_fund"
                    )
                
                # Current savings & investments section
                st.markdown("---")
                st.subheader("💰 Current Savings & Investments")
                st.markdown("If these weren't found in your CSV, enter them here:")
                
                curr_save_col1, curr_save_col2, curr_save_col3 = st.columns(3)
                with curr_save_col1:
                    current_savings = st.number_input(
                        "Current savings account (£)",
                        min_value=0,
                        max_value=10_000_000,
                        value=0,
                        step=1000,
                        key="current_savings",
                        help="Cash savings you have available"
                    )
                
                with curr_save_col2:
                    current_pensions = st.number_input(
                        "Pension balance (£)",
                        min_value=0,
                        max_value=10_000_000,
                        value=0,
                        step=1000,
                        key="current_pensions",
                        help="Total value of all pension pots"
                    )
                
                with curr_save_col3:
                    current_investments = st.number_input(
                        "Other investments (£)",
                        min_value=0,
                        max_value=10_000_000,
                        value=0,
                        step=1000,
                        key="current_investments",
                        help="ISAs, stocks, bonds, crypto, etc."
                    )
                
                total_current_assets = current_savings + current_pensions + current_investments
                if total_current_assets > 0:
                    st.success(f"💪 **Total current assets:** £{total_current_assets:,.0f}")
                
                # Note if savings was not detected in CSV
                if not has_savings_data:
                    st.info("ℹ️ No savings detected in your uploaded CSV. If you have savings/investments, please enter them above so we can factor them into your analysis.")
                
                st.markdown("---")
                
                # Calculate monthly savings needed for goals
                goals_monthly = {}
                
                # Children fund: £200-300/month per child for education, activities
                if num_children > 0:
                    goals_monthly["Children savings"] = num_children * 250
                
                # House deposit fund
                if buying_house and house_years > 0:
                    target_deposit = house_price * (deposit_pct / 100)
                    # Simplified: divide total by months remaining
                    goals_monthly["House deposit savings"] = target_deposit / (house_years * 12)
                
                # Car savings fund
                if buying_car and car_years > 0:
                    goals_monthly["Car purchase fund"] = car_price / (car_years * 12)
                
                # Emergency fund: (net income / 12) * emergency_fund_months / 12
                essential_annual = fixed_essentials * 12
                emergency_target = (essential_annual * emergency_fund_months) / 12
                goals_monthly["Emergency fund"] = emergency_target / 12
                
                # Add car running costs to the essential bucket if they're buying a car
                adjusted_fixed_essentials = fixed_essentials + car_running_costs_monthly
                
                if goals_monthly:
                    total_goals_monthly = sum(goals_monthly.values())
                    st.info(f"💡 **Monthly savings needed for goals:** £{total_goals_monthly:,.0f}")
                    
                    # Show car running costs note if applicable
                    if car_running_costs_monthly > 0:
                        st.info(f"🚗 **Car running costs added to Essential:** £{car_running_costs_monthly:,.0f}/month (included in allocation below)")
                    
                    goals_df = pd.DataFrame([
                        {"Goal": k, "Monthly": f"£{v:,.0f}", "Annual": f"£{v*12:,.0f}"}
                        for k, v in goals_monthly.items()
                    ])
                    st.dataframe(goals_df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Charts section in expander
            with st.expander("📊 Your Budget vs Recommended", expanded=True):
                chart_compare = pd.DataFrame({
                    "Your Budget": [parsed.get(b, 0) * 12 for b in rec_guideline.keys()],
                    "Recommended": [csv_net_income * pct for pct in rec_guideline.values()],
                }, index=rec_guideline.keys())
                
                chart_col1, chart_col2 = st.columns(2)
                with chart_col1:
                    st.bar_chart(chart_compare, height=320)
                with chart_col2:
                    st.line_chart(chart_compare, height=320)
            
            st.markdown("---")
            st.markdown("""
            **AI Analysis Tips**
            - **Low savings?** Redirect from lifestyle or review essential costs (housing, transport).
            - **High essentials?** Look for ways to reduce fixed costs or negotiate better rates.
            - **Surplus?** Reinvest into savings, pensions, or financial goals.
            """)

            # Detailed allocation strategies
            st.markdown("---")
            with st.expander("🧭 Detailed Allocation Strategies", expanded=True):
                strategies = {
                    "50/30/20 Envelope": {
                        "split": {"Essential": 0.50, "Children": 0.00, "Savings": 0.20, "Lifestyle": 0.30},
                        "notes": "Classic envelope method. Prioritises fixed essentials, keeps lifestyle flexible, and enforces a core savings habit.",
                    },
                    "High Savings + Emergency": {
                        "split": {"Essential": 0.55, "Children": 0.00, "Savings": 0.30, "Lifestyle": 0.15},
                        "notes": "Build emergency fund fast and accelerate investing/pensions while trimming lifestyle.",
                    },
                    "Family-Focused": {
                        "split": {"Essential": 0.50, "Children": 0.20, "Savings": 0.20, "Lifestyle": 0.10},
                        "notes": "Supports childcare/education while keeping savings steady and lifestyle lean.",
                    },
                    "Debt Snowball (Savings-as-debt)": {
                        "split": {"Essential": 0.50, "Children": 0.05, "Savings": 0.30, "Lifestyle": 0.15},
                        "notes": "Use the savings bucket for targeted extra debt repayments until cleared.",
                    },
                    "Conservative Essentials": {
                        "split": {"Essential": 0.60, "Children": 0.10, "Savings": 0.20, "Lifestyle": 0.10},
                        "notes": "Higher fixed costs environment. Protect savings and keep lifestyle controlled.",
                    },
                }

                strat_name = st.selectbox("Choose an allocation strategy", list(strategies.keys()), key="alloc_strategy")
                strat = strategies[strat_name]
                # Normalise split if needed
                total_split = sum(strat["split"].values())
                norm_split = {k: (v / total_split) for k, v in strat["split"].items()} if total_split > 0 else strat["split"]
                
                # Calculate flexible budget (net income minus fixed essentials, including car running costs)
                fixed_annual = adjusted_fixed_essentials * 12
                flexible_annual = max(csv_net_income - fixed_annual, 0)
            # Detailed sub-categories for each bucket
            # Build transport sub-category
            transport_subcats = {
                "Fixed (Rent/Tax/Utilities/Car)": adjusted_fixed_essentials,  # Lock in actual fixed costs including car running costs
                "Groceries & Food": 0.50,
                "Transport & Commute": 0.30,
                "Other Essential": 0.20,
            }
            
            sub_categories = {
                "Essential": transport_subcats,
                "Children": {
                    "Childcare": 0.40,
                    "Education & School": 0.30,
                    "Activities & Clubs": 0.15,
                    "Future Education Fund": 0.15,
                },
                "Savings": {
                    "Emergency Fund": 0.25,
                    "Pension Contributions": 0.35,
                    "House Deposit Fund": 0.25,
                    "Investments (ISA/Trading)": 0.15,
                },
                "Lifestyle": {
                    "Dining & Entertainment": 0.35,
                    "Leisure & Hobbies": 0.25,
                    "Travel & Holidays": 0.25,
                    "Subscriptions & Memberships": 0.10,
                    "Insurance & Protection": 0.05,
                },
            }

            alloc_rows = []
            rec_monthly = {}
            
            # Essential bucket: lock fixed costs, allocate flexible portion from flexible budget
            essential_pct = norm_split.get("Essential", 0.50)
            essential_annual = fixed_annual + (flexible_annual * essential_pct)
            essential_monthly = essential_annual / 12
            rec_monthly["Essential"] = essential_monthly
            
            alloc_rows.append({
                "Item": "💰 Essential",
                "% of Net": f"{(essential_annual/csv_net_income)*100 if csv_net_income else 0:.0f}%",
                "Monthly": f"£{essential_monthly:,.0f}",
                "Annual": f"£{essential_annual:,.0f}",
            })
            
            # Show each fixed essential item individually
            for fixed_item in fixed_essential_items:
                item_name = fixed_item["item"]
                item_monthly = fixed_item["monthly"]
                alloc_rows.append({
                    "Item": f"  🔒 {item_name}",
                    "% of Net": f"{(item_monthly*12/csv_net_income)*100:.1f}%",
                    "Monthly": f"£{item_monthly:,.0f}",
                    "Annual": f"£{item_monthly*12:,.0f}",
                })
            
            # Then flexible essentials
            flexible_essential = essential_monthly - fixed_essentials
            if flexible_essential > 0:
                for sub_item, sub_pct in {"Groceries & Food": 0.50, "Transport & Commute": 0.30, "Other Essential": 0.20}.items():
                    sub_monthly = flexible_essential * sub_pct
                    alloc_rows.append({
                        "Item": f"  └─ {sub_item}",
                        "% of Net": f"{(sub_monthly*12/csv_net_income)*100:.1f}%",
                        "Monthly": f"£{sub_monthly:,.0f}",
                        "Annual": f"£{sub_monthly*12:,.0f}",
                    })
            
            # Other buckets
            for bucket, pct in norm_split.items():
                if bucket == "Essential":
                    continue
                    
                # Allocate from flexible budget only (fixed already reserved)
                bucket_annual = flexible_annual * pct
                bucket_monthly = bucket_annual / 12
                rec_monthly[bucket] = bucket_monthly
                
                alloc_rows.append({
                    "Item": f"💰 {bucket}",
                    "% of Net": f"{(bucket_annual/csv_net_income)*100 if csv_net_income else 0:.0f}%",
                    "Monthly": f"£{bucket_monthly:,.0f}",
                    "Annual": f"£{bucket_annual:,.0f}",
                })
                
                # Special handling for Savings bucket: include life goals breakdown
                if bucket == "Savings" and goals_monthly:
                    # Allocate bucket budget to life goals first, then other savings
                    total_goals = sum(goals_monthly.values())
                    remaining_savings = bucket_monthly - total_goals if total_goals < bucket_monthly else 0
                    
                    # Show each goal
                    for goal_name, goal_amount in goals_monthly.items():
                        goal_pct = (goal_amount / bucket_monthly) if bucket_monthly > 0 else 0
                        alloc_rows.append({
                            "Item": f"  🎯 {goal_name}",
                            "% of Net": f"{(goal_amount*12/csv_net_income)*100 if csv_net_income else 0:.1f}%",
                            "Monthly": f"£{goal_amount:,.0f}",
                            "Annual": f"£{goal_amount*12:,.0f}",
                        })
                    
                    # Show remaining savings items
                    if remaining_savings > 0:
                        for sub_item, sub_pct in {"Pension Contributions": 0.50, "Investments (ISA/Trading)": 0.50}.items():
                            sub_monthly = remaining_savings * sub_pct
                            alloc_rows.append({
                                "Item": f"  └─ {sub_item}",
                                "% of Net": f"{(sub_monthly*12/csv_net_income)*100 if csv_net_income else 0:.1f}%",
                                "Monthly": f"£{sub_monthly:,.0f}",
                                "Annual": f"£{sub_monthly*12:,.0f}",
                            })
                elif bucket in sub_categories:
                    for sub_item, sub_pct in sub_categories[bucket].items():
                        sub_monthly = bucket_monthly * sub_pct
                        alloc_rows.append({
                            "Item": f"  └─ {sub_item}",
                            "% of Net": f"{(pct * sub_pct)*100:.1f}%",
                            "Monthly": f"£{sub_monthly:,.0f}",
                            "Annual": f"£{sub_monthly*12:,.0f}",
                        })
            
            strat_df = pd.DataFrame(alloc_rows)
            st.dataframe(strat_df, hide_index=True, use_container_width=True)
            st.caption(strat["notes"])
            
            # AI analysis of goal feasibility against this strategy - Optional
            if goals_monthly and client:
                st.markdown("---")
                show_goal_analysis = st.checkbox("🎯 Analyze goal feasibility with AI", value=False, key="show_goal_analysis")
                if show_goal_analysis:
                    with st.spinner("🤖 Analyzing goal feasibility..."):
                        goals_summary = "\n".join([f"  - {k}: £{v:,.2f}/month (£{v*12:,.2f}/year)" for k, v in goals_monthly.items()])
                        available_savings = rec_monthly.get("Savings", 0)
                        goals_analysis = analyze_goals_feasibility_with_ai(
                            goals_summary, available_savings, csv_net_income, fixed_essentials
                        )
                    if goals_analysis:
                        st.markdown("### 🎯 Life Goals Feasibility Analysis")
                        st.markdown(goals_analysis)
                    
                    # Show a warning if goals exceed savings budget
                    total_goals = sum(goals_monthly.values())
                    savings_budget = rec_monthly.get("Savings", 0)
                    if total_goals > savings_budget:
                        shortfall = total_goals - savings_budget
                        st.warning(
                            f"⚠️ **Goals exceed allocated savings budget:**\n\n"
                            f"Your goals need **£{total_goals:,.0f}/month**, but the {strat_name} strategy allocates **£{savings_budget:,.0f}/month** to savings.\n\n"
                            f"**Monthly shortfall: £{shortfall:,.0f}**\n\n"
                            f"Consider: reducing lifestyle spending, choosing a higher-savings strategy, or extending your goal timelines."
                        )

            st.markdown("---")
            
            # AI summary of the chosen strategy recommendation - Optional
            rec_month_income = csv_net_income / 12
            show_recommendation_summary = st.checkbox("🤖 Show AI recommendation summary", value=False, key="show_rec_summary")
            if show_recommendation_summary and client:
                with st.spinner("🤖 Summarising the recommended plan..."):
                    rec_summary = "\n".join([
                        f"  - {bucket}: £{amount:,.2f}/month ({(amount/rec_month_income*100):.1f}% of income)" 
                        for bucket, amount in rec_monthly.items()
                    ])
                    ai_summary = analyze_budget_with_ai(rec_summary, csv_net_income)
                if ai_summary:
                    st.markdown("### 🤖 AI Recommendation Summary")
                    st.markdown(ai_summary)

            # Export: example CSV using the recommended split (detailed format)
            st.markdown("---")
            
            with st.expander("💡 Your Recommended Monthly Allocation", expanded=True):
                st.markdown(f"**Total monthly net income:** £{csv_net_income/12:,.2f}")
                
                rec_month_income = csv_net_income / 12
                
                # Validate that allocation totals match income
                total_allocated = sum(rec_monthly.values())
                if abs(total_allocated - rec_month_income) > 1:  # Allow 1p rounding
                    st.warning(
                        f"⚠️ **Allocation mismatch detected:**\n"
                        f"Total allocated: £{total_allocated:,.2f}\n"
                        f"Actual income: £{rec_month_income:,.2f}\n"
                        f"Difference: £{rec_month_income - total_allocated:,.2f}"
                    )
                
                export_rows = [
                    {"Description": "Description", "Your Current (£)": "Your Current (£)", "Recommended (£)": "Recommended (£)", "Difference (£)": "Difference (£)", "Weekly": "Weekly"},
                    {"Description": "Monthly Income (£)", "Your Current (£)": f"£{rec_month_income:,.2f}", "Recommended (£)": f"£{rec_month_income:,.2f}", "Difference (£)": "—", "Weekly": f"£{rec_month_income/4.33:,.2f}"},
                ]
                
                # Add Essential bucket with granular fixed items
                actual_essential = parsed.get("Essential", 0)
                export_rows.append({
                    "Description": "\nEssential",
                    "Your Current (£)": f"£{actual_essential:,.2f}",
                    "Recommended (£)": f"£{rec_monthly.get('Essential', 0):,.2f}",
                    "Difference (£)": f"£{rec_monthly.get('Essential', 0) - actual_essential:,.2f}",
                    "Weekly": "",
                })
                
                # Add each fixed essential item individually
                for fixed_item in fixed_essential_items:
                    item_name = fixed_item["item"]
                    item_monthly = fixed_item["monthly"]
                    weekly_amt = item_monthly / 4.33
                    export_rows.append({
                        "Description": f"  - {item_name}",
                        "Your Current (£)": f"£{item_monthly:,.2f}",
                        "Recommended (£)": f"£{item_monthly:,.2f}",
                        "Difference (£)": "—",
                        "Weekly": f"£{weekly_amt:,.2f}",
                    })
                
                # Flexible essential items
                flexible_essential = rec_monthly.get("Essential", 0) - fixed_essentials
                if flexible_essential > 0:
                    for sub_item, sub_pct in {"Groceries & Food": 0.50, "Transport & Commute": 0.30, "Other Essential": 0.20}.items():
                        sub_monthly = flexible_essential * sub_pct
                        weekly_amt = sub_monthly / 4.33
                        export_rows.append({
                            "Description": f"  - {sub_item}",
                            "Your Current (£)": "—",
                            "Recommended (£)": f"£{sub_monthly:,.2f}",
                            "Difference (£)": "—",
                            "Weekly": f"£{weekly_amt:,.2f}",
                        })
                
                # Add car costs breakdown if applicable (from manual entry)
                if car_costs_monthly > 0 and car_breakdown:
                    export_rows.append({
                        "Description": f"  - 🚗 Car Costs ({num_cars} car{'s' if num_cars != 1 else ''})",
                        "Your Current (£)": "—",
                        "Recommended (£)": f"£{car_costs_monthly:,.2f}",
                        "Difference (£)": "—",
                        "Weekly": f"£{car_costs_monthly/4.33:,.2f}",
                    })
                    for item, monthly_cost in car_breakdown.items():
                        weekly_amt = monthly_cost / 4.33
                        export_rows.append({
                            "Description": f"    - {item.title()}",
                            "Your Current (£)": "—",
                            "Recommended (£)": f"£{monthly_cost:,.2f}",
                            "Difference (£)": "—",
                            "Weekly": f"£{weekly_amt:,.2f}",
                        })
                
                # Other buckets
                for bucket in ["Children", "Savings", "Lifestyle"]:
                    if bucket in rec_monthly and rec_monthly[bucket] > 0:
                        actual_bucket = parsed.get(bucket, 0)
                        export_rows.append({
                            "Description": f"\n{bucket}",
                            "Your Current (£)": f"£{actual_bucket:,.2f}",
                            "Recommended (£)": f"£{rec_monthly[bucket]:,.2f}",
                            "Difference (£)": f"£{rec_monthly[bucket] - actual_bucket:,.2f}",
                            "Weekly": "",
                        })
                        
                        # Special handling for Savings: include life goals, capped to available budget
                        if bucket == "Savings" and goals_monthly:
                            savings_budget = rec_monthly[bucket]
                            total_goals = sum(goals_monthly.values())
                            
                            # Cap goals to available budget
                            goal_amounts = {}
                            if total_goals <= savings_budget:
                                # All goals fit - allocate as requested
                                goal_amounts = goals_monthly.copy()
                            else:
                                # Goals exceed budget - scale them down proportionally
                                scale_factor = savings_budget / total_goals
                                goal_amounts = {k: v * scale_factor for k, v in goals_monthly.items()}
                            
                            remaining_savings = savings_budget - sum(goal_amounts.values())
                            
                            # Add each goal as a line item
                            for goal_name, goal_amount in goal_amounts.items():
                                weekly_amt = goal_amount / 4.33
                                export_rows.append({
                                    "Description": f"  - {goal_name}",
                                    "Your Current (£)": "—",
                                    "Recommended (£)": f"£{goal_amount:,.2f}",
                                    "Difference (£)": "—",
                                    "Weekly": f"£{weekly_amt:,.2f}",
                                })
                            
                            # Add remaining savings items
                            if remaining_savings > 1:  # Only show if > £1
                                for sub_item, sub_pct in {"Pension Contributions": 0.50, "Investments (ISA/Trading)": 0.50}.items():
                                    sub_monthly = remaining_savings * sub_pct
                                    weekly_amt = sub_monthly / 4.33
                                    export_rows.append({
                                        "Description": f"  - {sub_item}",
                                        "Your Current (£)": "—",
                                        "Recommended (£)": f"£{sub_monthly:,.2f}",
                                        "Difference (£)": "—",
                                        "Weekly": f"£{weekly_amt:,.2f}",
                                    })
                        elif bucket in sub_categories:
                            for sub_item, sub_pct in sub_categories[bucket].items():
                                sub_monthly = rec_monthly[bucket] * sub_pct
                                weekly_amt = sub_monthly / 4.33
                                export_rows.append({
                                    "Description": f"  - {sub_item}",
                                    "Your Current (£)": "—",
                                    "Recommended (£)": f"£{sub_monthly:,.2f}",
                                    "Difference (£)": "—",
                                    "Weekly": f"£{weekly_amt:,.2f}",
                                })
                
                export_rows.append({
                    "Description": "\nTotal Recommended",
                    "Your Current (£)": f"£{rec_month_income:,.2f}",
                    "Recommended (£)": f"£{rec_month_income:,.2f}",
                    "Difference (£)": "—",
                    "Weekly": f"£{rec_month_income/4.33:,.2f}",
                })

                export_df = pd.DataFrame(export_rows)
                st.dataframe(export_df, hide_index=True, use_container_width=True)
                
                csv_bytes = export_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="📥 Download as CSV",
                    data=csv_bytes,
                    file_name="recommended_budget.csv",
                    mime="text/csv",
                )
            
            # AI analysis of the recommended allocation
            if client:
                with st.spinner("🤖 Analyzing your recommended allocation..."):
                    allocation_analysis = analyze_recommended_allocation_with_ai(
                        rec_monthly, csv_net_income, fixed_essentials, parsed
                    )
                if allocation_analysis:
                    with st.expander("🤖 Allocation Analysis & Next Steps", expanded=True):
                        st.markdown(allocation_analysis)
            
            st.markdown("---")
            
            # TWO COMPREHENSIVE PLANS
            st.header("📋 Your Two Allocation Plans")
            st.markdown("We've created two plans for you. Choose based on your priorities:")
            
            plan_choice = st.radio(
                "Which plan would you like to see?",
                ["🛡️ **Safe/Conservative Plan** (Financial health first)", 
                 "🎯 **Goals-Focused Plan** (Achieve your dreams)"],
                horizontal=True,
                key="plan_choice"
            )
            
            rec_month_income = csv_net_income / 12
            
            if "Safe/Conservative" in plan_choice:
                with st.expander("🛡️ Safe & Conservative Plan (Financially Optimal)", expanded=True):
                    st.markdown("""
This plan **ignores your wants and focuses on your financial health**. It's designed to:
- ✅ Build a strong financial foundation
- ✅ Maximize financial security and flexibility
- ✅ Eliminate financial stress
- ✅ Enable you to weather emergencies
- ✅ Give you options and freedom in the future

**This plan assumes you'll minimize lifestyle spending and prioritize financial stability.**
                    """)
                    
                    # Conservative allocation: maximize savings & essentials, minimize lifestyle
                    safe_plan = {
                        "Essential": fixed_essentials * 12 + (flexible_annual * 0.20),  # Essential + some flexibility
                        "Children": flexible_annual * (0.15 if num_children > 0 else 0.05),  # Only if you have kids
                        "Savings": flexible_annual * 0.55,  # Heavily weighted to savings
                        "Lifestyle": flexible_annual * 0.10,  # Minimised lifestyle
                    }
                    
                    safe_plan = {k: v/12 for k, v in safe_plan.items()}  # Convert to monthly
                    
                    # Build granular allocation table for Safe Plan
                    safe_detailed_rows = [
                        {"Line Item": "💰 MONTHLY NET INCOME", "Monthly": f"£{rec_month_income:,.2f}", "Weekly": f"£{rec_month_income/4.33:,.2f}", "Annual": f"£{rec_month_income*12:,.0f}", "% of Income": "100%", "Notes": "Your total take-home"},
                        {"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""},
                    ]
                    
                    # ESSENTIAL - Fixed costs first
                    safe_detailed_rows.append({"Line Item": "🔒 ESSENTIAL COSTS (Fixed/Non-negotiable)", "Monthly": f"£{fixed_essentials:,.2f}", "Weekly": f"£{fixed_essentials/4.33:,.2f}", "Annual": f"£{fixed_essentials*12:,.0f}", "% of Income": f"{(fixed_essentials/rec_month_income*100):.1f}%", "Notes": "Housing, utilities, essentials"})
                    
                    for fixed_item in fixed_essential_items:
                        safe_detailed_rows.append({
                            "Line Item": f"  └─ {fixed_item['item']}",
                            "Monthly": f"£{fixed_item['monthly']:,.2f}",
                            "Weekly": f"£{fixed_item['monthly']/4.33:,.2f}",
                            "Annual": f"£{fixed_item['monthly']*12:,.0f}",
                            "% of Income": f"{(fixed_item['monthly']/rec_month_income*100):.1f}%",
                            "Notes": "Locked in"
                        })
                    
                    # Flexible essentials
                    flexible_essential_amt = safe_plan['Essential'] - fixed_essentials
                    if flexible_essential_amt > 0:
                        safe_detailed_rows.append({"Line Item": "✏️ ESSENTIAL - Flexible Portion", "Monthly": f"£{flexible_essential_amt:,.2f}", "Weekly": f"£{flexible_essential_amt/4.33:,.2f}", "Annual": f"£{flexible_essential_amt*12:,.0f}", "% of Income": f"{(flexible_essential_amt/rec_month_income*100):.1f}%", "Notes": "Food, transport, discretionary essentials"})
                        
                        flex_essential_sub = {
                            "Groceries & Food": flexible_essential_amt * 0.55,
                            "Transport & Commute": flexible_essential_amt * 0.30,
                            "Other Essentials": flexible_essential_amt * 0.15,
                        }
                        for item, amt in flex_essential_sub.items():
                            safe_detailed_rows.append({
                                "Line Item": f"  └─ {item}",
                                "Monthly": f"£{amt:,.2f}",
                                "Weekly": f"£{amt/4.33:,.2f}",
                                "Annual": f"£{amt*12:,.0f}",
                                "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                                "Notes": "Allocate as needed"
                            })
                    
                    safe_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    
                    # CHILDREN
                    if safe_plan['Children'] > 0:
                        safe_detailed_rows.append({"Line Item": "👶 CHILDREN & DEPENDENTS", "Monthly": f"£{safe_plan['Children']:,.2f}", "Weekly": f"£{safe_plan['Children']/4.33:,.2f}", "Annual": f"£{safe_plan['Children']*12:,.0f}", "% of Income": f"{(safe_plan['Children']/rec_month_income*100):.1f}%", "Notes": "Education, activities, childcare"})
                        
                        children_sub = {
                            "Childcare/Nursery": safe_plan['Children'] * 0.50,
                            "School/Education": safe_plan['Children'] * 0.30,
                            "Activities & Extras": safe_plan['Children'] * 0.20,
                        }
                        for item, amt in children_sub.items():
                            safe_detailed_rows.append({
                                "Line Item": f"  └─ {item}",
                                "Monthly": f"£{amt:,.2f}",
                                "Weekly": f"£{amt/4.33:,.2f}",
                                "Annual": f"£{amt*12:,.0f}",
                                "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                                "Notes": "Essential child costs"
                            })
                        safe_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    
                    # SAVINGS - The priority
                    safe_detailed_rows.append({"Line Item": "💎 SAVINGS & INVESTMENTS (Your Priority)", "Monthly": f"£{safe_plan['Savings']:,.2f}", "Weekly": f"£{safe_plan['Savings']/4.33:,.2f}", "Annual": f"£{safe_plan['Savings']*12:,.0f}", "% of Income": f"{(safe_plan['Savings']/rec_month_income*100):.1f}%", "Notes": "Build wealth & security"})
                    
                    savings_sub = {
                        "Emergency Fund (3-6 months)": safe_plan['Savings'] * 0.30,
                        "Pension Contributions": safe_plan['Savings'] * 0.40,
                        "House/Investment Fund": safe_plan['Savings'] * 0.20,
                        "Stocks/ISA/Bonds": safe_plan['Savings'] * 0.10,
                    }
                    for item, amt in savings_sub.items():
                        safe_detailed_rows.append({
                            "Line Item": f"  └─ {item}",
                            "Monthly": f"£{amt:,.2f}",
                            "Weekly": f"£{amt/4.33:,.2f}",
                            "Annual": f"£{amt*12:,.0f}",
                            "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                            "Notes": "Pay yourself first"
                        })
                    
                    safe_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    
                    # LIFESTYLE - Minimized
                    safe_detailed_rows.append({"Line Item": "🎉 LIFESTYLE & DISCRETIONARY", "Monthly": f"£{safe_plan['Lifestyle']:,.2f}", "Weekly": f"£{safe_plan['Lifestyle']/4.33:,.2f}", "Annual": f"£{safe_plan['Lifestyle']*12:,.0f}", "% of Income": f"{(safe_plan['Lifestyle']/rec_month_income*100):.1f}%", "Notes": "Entertainment, dining, hobbies"})
                    
                    lifestyle_sub = {
                        "Dining Out": safe_plan['Lifestyle'] * 0.40,
                        "Entertainment": safe_plan['Lifestyle'] * 0.30,
                        "Hobbies & Personal": safe_plan['Lifestyle'] * 0.20,
                        "Subscriptions": safe_plan['Lifestyle'] * 0.10,
                    }
                    for item, amt in lifestyle_sub.items():
                        safe_detailed_rows.append({
                            "Line Item": f"  └─ {item}",
                            "Monthly": f"£{amt:,.2f}",
                            "Weekly": f"£{amt/4.33:,.2f}",
                            "Annual": f"£{amt*12:,.0f}",
                            "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                            "Notes": "Keep minimal"
                        })
                    
                    safe_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    safe_detailed_rows.append({
                        "Line Item": "✅ TOTAL ALLOCATED",
                        "Monthly": f"£{rec_month_income:,.2f}",
                        "Weekly": f"£{rec_month_income/4.33:,.2f}",
                        "Annual": f"£{rec_month_income*12:,.0f}",
                        "% of Income": "100%",
                        "Notes": "All income allocated"
                    })
                    
                    safe_df = pd.DataFrame(safe_detailed_rows)
                    st.dataframe(safe_df, hide_index=True, use_container_width=True)
                    
                    st.warning(f"""
**What this means for your goals:**
- House purchase: Extended timeline (6-8 years instead of 5)
- Car purchase: May need to buy cheaper used car or extend timeline to {max(3, car_years + 2)} years
- Lifestyle: Very limited holidays, dining out, entertainment
- BUT: You'll have £{safe_plan['Savings']*12:,.0f}/year for emergencies, pensions, and building wealth

**Red flags you'll avoid:**
- ❌ Overdraft/debt (you'll have buffer)
- ❌ Financial stress (savings cushion)
- ❌ Unable to handle emergencies (strong emergency fund)
- ❌ Missing pension contributions (prioritized)
                    """)
                    
            else:  # Goals-Focused Plan
                with st.expander("🎯 Goals-Focused Plan (Achieve Your Dreams)", expanded=True):
                    st.markdown("""
This plan **balances your goals with financial health**. It's designed to:
- ✅ Help you achieve your life goals
- ✅ Allow reasonable lifestyle spending
- ✅ Maintain financial stability
- ✅ Extend timelines where needed for realism

**This plan acknowledges your wants and finds realistic ways to achieve them.**
                    """)
                    
                    # Goals-focused: balance savings with goals and lifestyle
                    goals_plan = {
                        "Essential": fixed_essentials * 12 + (flexible_annual * 0.15),  # Essential + slight flexibility
                        "Children": flexible_annual * (0.20 if num_children > 0 else 0.05),
                        "Savings": flexible_annual * 0.40,  # 40% for goals + emergency fund
                        "Lifestyle": flexible_annual * 0.25,  # More realistic lifestyle budget
                    }
                    
                    goals_plan = {k: v/12 for k, v in goals_plan.items()}  # Convert to monthly
                    
                    # Build granular allocation table for Goals Plan
                    goals_detailed_rows = [
                        {"Line Item": "💰 MONTHLY NET INCOME", "Monthly": f"£{rec_month_income:,.2f}", "Weekly": f"£{rec_month_income/4.33:,.2f}", "Annual": f"£{rec_month_income*12:,.0f}", "% of Income": "100%", "Notes": "Your total take-home"},
                        {"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""},
                    ]
                    
                    # ESSENTIAL - Fixed costs first
                    goals_detailed_rows.append({"Line Item": "🔒 ESSENTIAL COSTS (Fixed/Non-negotiable)", "Monthly": f"£{fixed_essentials:,.2f}", "Weekly": f"£{fixed_essentials/4.33:,.2f}", "Annual": f"£{fixed_essentials*12:,.0f}", "% of Income": f"{(fixed_essentials/rec_month_income*100):.1f}%", "Notes": "Housing, utilities, essentials"})
                    
                    for fixed_item in fixed_essential_items:
                        goals_detailed_rows.append({
                            "Line Item": f"  └─ {fixed_item['item']}",
                            "Monthly": f"£{fixed_item['monthly']:,.2f}",
                            "Weekly": f"£{fixed_item['monthly']/4.33:,.2f}",
                            "Annual": f"£{fixed_item['monthly']*12:,.0f}",
                            "% of Income": f"{(fixed_item['monthly']/rec_month_income*100):.1f}%",
                            "Notes": "Locked in"
                        })
                    
                    # Flexible essentials
                    flexible_essential_amt = goals_plan['Essential'] - fixed_essentials
                    if flexible_essential_amt > 0:
                        goals_detailed_rows.append({"Line Item": "✏️ ESSENTIAL - Flexible Portion", "Monthly": f"£{flexible_essential_amt:,.2f}", "Weekly": f"£{flexible_essential_amt/4.33:,.2f}", "Annual": f"£{flexible_essential_amt*12:,.0f}", "% of Income": f"{(flexible_essential_amt/rec_month_income*100):.1f}%", "Notes": "Food, transport, discretionary essentials"})
                        
                        flex_essential_sub = {
                            "Groceries & Food": flexible_essential_amt * 0.55,
                            "Transport & Commute": flexible_essential_amt * 0.30,
                            "Other Essentials": flexible_essential_amt * 0.15,
                        }
                        for item, amt in flex_essential_sub.items():
                            goals_detailed_rows.append({
                                "Line Item": f"  └─ {item}",
                                "Monthly": f"£{amt:,.2f}",
                                "Weekly": f"£{amt/4.33:,.2f}",
                                "Annual": f"£{amt*12:,.0f}",
                                "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                                "Notes": "Allocate as needed"
                            })
                    
                    goals_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    
                    # CHILDREN
                    if goals_plan['Children'] > 0:
                        goals_detailed_rows.append({"Line Item": "👶 CHILDREN & DEPENDENTS", "Monthly": f"£{goals_plan['Children']:,.2f}", "Weekly": f"£{goals_plan['Children']/4.33:,.2f}", "Annual": f"£{goals_plan['Children']*12:,.0f}", "% of Income": f"{(goals_plan['Children']/rec_month_income*100):.1f}%", "Notes": "Education, activities, childcare"})
                        
                        children_sub = {
                            "Childcare/Nursery": goals_plan['Children'] * 0.50,
                            "School/Education": goals_plan['Children'] * 0.30,
                            "Activities & Extras": goals_plan['Children'] * 0.20,
                        }
                        for item, amt in children_sub.items():
                            goals_detailed_rows.append({
                                "Line Item": f"  └─ {item}",
                                "Monthly": f"£{amt:,.2f}",
                                "Weekly": f"£{amt/4.33:,.2f}",
                                "Annual": f"£{amt*12:,.0f}",
                                "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                                "Notes": "Essential child costs"
                            })
                        goals_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    
                    # SAVINGS - Balanced for goals AND security
                    goals_detailed_rows.append({"Line Item": "💎 SAVINGS & GOAL FUNDING", "Monthly": f"£{goals_plan['Savings']:,.2f}", "Weekly": f"£{goals_plan['Savings']/4.33:,.2f}", "Annual": f"£{goals_plan['Savings']*12:,.0f}", "% of Income": f"{(goals_plan['Savings']/rec_month_income*100):.1f}%", "Notes": "Goals + security"})
                    
                    # Build goal savings allocations dynamically
                    savings_sub = {
                        "Emergency Fund (3-6 months)": goals_plan['Savings'] * 0.20,
                        "Pension Contributions": goals_plan['Savings'] * 0.25,
                    }
                    
                    # Add life goals if applicable
                    if buying_car and car_price > 0:
                        car_monthly_target = car_price / (car_years * 12) if car_years > 0 else 0
                        savings_sub["🚗 Car Purchase Fund"] = car_monthly_target
                    
                    if buying_house and house_price > 0:
                        deposit_needed = house_price * (deposit_pct / 100)
                        house_monthly_target = deposit_needed / (house_years * 12) if house_years > 0 else 0
                        savings_sub["🏠 House Deposit Fund"] = house_monthly_target
                    
                    # Remaining for ISA/investments
                    remaining_savings = goals_plan['Savings'] - sum([v for k, v in savings_sub.items() if not k.startswith("🚗") and not k.startswith("🏠")])
                    remaining_savings = remaining_savings - (goals_plan['Savings'] * 0.20) - (goals_plan['Savings'] * 0.25)
                    if remaining_savings > 0:
                        savings_sub["Stocks/ISA/Bonds"] = remaining_savings
                    
                    for item, amt in savings_sub.items():
                        if amt > 0:
                            goals_detailed_rows.append({
                                "Line Item": f"  └─ {item}",
                                "Monthly": f"£{amt:,.2f}",
                                "Weekly": f"£{amt/4.33:,.2f}",
                                "Annual": f"£{amt*12:,.0f}",
                                "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                                "Notes": "Progress on your goals"
                            })
                    
                    goals_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    
                    # LIFESTYLE - Realistic and Healthy
                    goals_detailed_rows.append({"Line Item": "🎉 LIFESTYLE & ENJOYMENT", "Monthly": f"£{goals_plan['Lifestyle']:,.2f}", "Weekly": f"£{goals_plan['Lifestyle']/4.33:,.2f}", "Annual": f"£{goals_plan['Lifestyle']*12:,.0f}", "% of Income": f"{(goals_plan['Lifestyle']/rec_month_income*100):.1f}%", "Notes": "Balance & quality of life"})
                    
                    lifestyle_sub = {
                        "Dining Out & Coffee": goals_plan['Lifestyle'] * 0.35,
                        "Holidays & Travel": goals_plan['Lifestyle'] * 0.30,
                        "Hobbies & Entertainment": goals_plan['Lifestyle'] * 0.20,
                        "Subscriptions & Memberships": goals_plan['Lifestyle'] * 0.15,
                    }
                    for item, amt in lifestyle_sub.items():
                        goals_detailed_rows.append({
                            "Line Item": f"  └─ {item}",
                            "Monthly": f"£{amt:,.2f}",
                            "Weekly": f"£{amt/4.33:,.2f}",
                            "Annual": f"£{amt*12:,.0f}",
                            "% of Income": f"{(amt/rec_month_income*100):.1f}%",
                            "Notes": "Enjoy your life"
                        })
                    
                    goals_detailed_rows.append({"Line Item": "", "Monthly": "", "Weekly": "", "Annual": "", "% of Income": "", "Notes": ""})
                    goals_detailed_rows.append({
                        "Line Item": "✅ TOTAL ALLOCATED",
                        "Monthly": f"£{rec_month_income:,.2f}",
                        "Weekly": f"£{rec_month_income/4.33:,.2f}",
                        "Annual": f"£{rec_month_income*12:,.0f}",
                        "% of Income": "100%",
                        "Notes": "All income allocated"
                    })
                    
                    goals_df = pd.DataFrame(goals_detailed_rows)
                    st.dataframe(goals_df, hide_index=True, use_container_width=True)
                    
                    # Calculate adjusted goal timelines with this budget
                    monthly_for_goals = goals_plan['Savings']
                    goal_timeline_msg = ""
                    
                    if buying_car and car_price > 0:
                        months_to_car = car_price / (monthly_for_goals * 0.30)  # 30% of savings to car
                        years_to_car = months_to_car / 12
                        goal_timeline_msg += f"\n- **Car**: £{car_price:,.0f} at {(monthly_for_goals * 0.30):,.0f}/month = **{years_to_car:.1f} years**"
                    
                    if buying_house and house_price > 0:
                        target_deposit = house_price * (deposit_pct / 100)
                        months_to_house = target_deposit / (monthly_for_goals * 0.40)  # 40% of savings to house
                        years_to_house = months_to_house / 12
                        goal_timeline_msg += f"\n- **House**: £{target_deposit:,.0f} deposit at {(monthly_for_goals * 0.40):,.0f}/month = **{years_to_house:.1f} years**"
                    
                    if monthly_for_goals * 0.30 > 0:
                        goal_timeline_msg += f"\n- **Emergency fund**: Build 3-6 months expenses = ~1 year"
                    
                    st.info(f"""
**Realistic timeline for your goals with this budget:**{goal_timeline_msg}

**Your lifestyle budget:**
- Monthly: £{goals_plan['Lifestyle']:,.2f} (~£{goals_plan['Lifestyle']/4.33:,.2f}/week)
- Annual: £{goals_plan['Lifestyle']*12:,.2f}
- This allows ~1 holiday/year, regular dining out, hobbies, entertainment

**Monthly breakdown of {goals_plan['Savings']:,.2f} savings:**
- Emergency fund: £{monthly_for_goals * 0.15:,.2f}
- Pension: £{monthly_for_goals * 0.25:,.2f}
- Life goals (house/car): £{monthly_for_goals * 0.50:,.2f}
- Other investments: £{monthly_for_goals * 0.10:,.2f}
                    """)
            
            st.markdown("---")
            
            # Prepare context for AI chat
            context_summary = f"""
Your Financial Profile:
- Monthly net income: £{csv_net_income/12:,.2f}
- Current essential costs: £{fixed_essentials:,.2f}/month
- Recommended Monthly Allocation:
  - Essential: £{rec_monthly.get('Essential', 0):,.2f}
  - Children: £{rec_monthly.get('Children', 0):,.2f}
  - Savings: £{rec_monthly.get('Savings', 0):,.2f}
  - Lifestyle: £{rec_monthly.get('Lifestyle', 0):,.2f}
  
Your Current Spending:
{'; '.join([f'{k}: £{v:,.2f}/month' for k, v in parsed.items()])}

Analysis provided above describes your allocation and recommendations.
"""
            
            # Render AI chat for questions about the allocation
            render_allocation_ai_chat(context_summary)
    else:
        st.info("👆 Upload a CSV to see your budget analysis and AI recommendations.")
        
        with st.expander("📋 Example CSV format"):
            st.markdown("""
            Your CSV should have at least 2 columns:
            
            | bucket | monthly |
            |--------|---------|
            | Rent | 1500 |
            | Utilities | 200 |
            | Groceries | 500 |
            | Childcare | 800 |
            | Pension | 400 |
            | Holidays | 300 |
            
            Or use **'annual'** instead of **'monthly'**. Bucket names are auto-mapped:
            - "rent", "housing" → Essential
            - "childcare", "education" → Children
            - "pension", "savings" → Savings
            - "holidays", "travel" → Lifestyle
            """)

