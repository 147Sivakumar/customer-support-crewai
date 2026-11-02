
import streamlit as st
from pathlib import Path
import re

# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="TechNova Support Dashboard",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------
# PROJECT PATHS
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "logs" / "customer_support_history.txt"
DATA_DIR = BASE_DIR / "data"

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }

    [data-testid="stSidebar"] {
        background-color: #14213d;
    }

    [data-testid="stSidebar"] * {
        color: white !important;
    }

    .main-title {
        font-size: 30px;
        font-weight: 700;
        color: #14213d;
    }

    .subtitle {
        color: #64748b;
        font-size: 14px;
    }

    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .metric-label {
        color: #64748b;
        font-size: 14px;
    }

    .metric-value {
        color: #14213d;
        font-size: 30px;
        font-weight: 700;
    }
</style>
""", unsafe_allow_html=True)


# -----------------------------------
# READ CUSTOMER SUPPORT LOGS
# -----------------------------------

def load_tickets():

    if not LOG_FILE.exists():
        return []

    content = LOG_FILE.read_text(encoding="utf-8")

    blocks = re.split(r"CUSTOMER SUPPORT INTERACTION", content)

    tickets = []

    for block in blocks[1:]:

        def extract(pattern):
            match = re.search(pattern, block, re.DOTALL)
            return match.group(1).strip() if match else ""

        ticket = {
            "date": extract(r"Date\s*:\s*([^\r\n]+)"),
            "time": extract(r"Time\s*:\s*([^\r\n]+)"),
            "customer": extract(r"Customer\s*:\s*([^\r\n]+)"),
            "agent": extract(r"Answered By:\s*([^\r\n]+)"),
            "response": extract(r"Response:\s*(.*?)\s*Status\s*:"),
            "status": extract(r"Status\s*:\s*([^\r\n]+)")
        }

        if ticket["customer"]:
            tickets.append(ticket)

    return tickets


# -----------------------------------
# LOAD TICKETS AND CALCULATE STATISTICS
# -----------------------------------

tickets = load_tickets()

total_tickets = len(tickets)

resolved_tickets = sum(
    1 for ticket in tickets
    if ticket["status"] == "Answered"
)

external_tickets = sum(
    1 for ticket in tickets
    if "External Research" in ticket["status"]
)

pending_tickets = sum(
    1 for ticket in tickets
    if "Confirmation" in ticket["status"]
)



# -----------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------

with st.sidebar:

    st.markdown("# 🎧 TechNova")
    st.caption("CUSTOMER SUPPORT CENTER")

    st.divider()

    page = st.radio(
        "MAIN MENU",
        [
            "Overview",
            "New Customer Query",
            "Ticket History",
            "Knowledge Base"
        ]
    )

    st.divider()

    st.markdown("### 🤖 AI SUPPORT SYSTEM")
    st.caption("Agent 01 — RAG Knowledge Agent")
    st.caption("Agent 02 — Internet Research Agent")
    st.caption("Agent 03 — Support Log Agent")

    st.divider()

    st.caption("TechNova Solutions")
    st.caption("AI Customer Support Automation")


# -----------------------------------
# OVERVIEW PAGE
# -----------------------------------

if page == "Overview":

    st.markdown(
        '<div class="main-title">Support Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Monitor customer interactions and AI agent activity.</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "Total Tickets", total_tickets),
        (col2, "Resolved Tickets", resolved_tickets),
        (col3, "External Research", external_tickets),
        (col4, "Pending Confirmation", pending_tickets)
    ]

    for column, label, value in metrics:

        with column:

            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{label}</div>
                    <div class="metric-value">{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.write("")
    st.subheader("AI Agent Status")

    agent_col1, agent_col2, agent_col3 = st.columns(3)

    with agent_col1:
        st.success("Agent 01 — RAG Knowledge Agent")
        st.caption("Retrieves answers from company documents.")

    with agent_col2:
        st.success("Agent 02 — Internet Research Agent")
        st.caption("Searches the internet when internal information is insufficient.")

    with agent_col3:
        st.success("Agent 03 — Support Log Agent")
        st.caption("Records customer interactions.")

    st.write("")
    st.subheader("Recent Customer Interactions")

    if tickets:

        recent_tickets = list(reversed(tickets[-5:]))

        for ticket in recent_tickets:

            with st.container(border=True):

                st.markdown(f"**{ticket['customer']}**")

                st.caption(
                    f"{ticket['date']} | {ticket['time']} | "
                    f"{ticket['agent']}"
                )

                st.write(f"Status: {ticket['status']}")

    else:
        st.info("No customer interactions recorded yet.")


# -----------------------------------
# NEW CUSTOMER QUERY PAGE
# -----------------------------------

elif page == "New Customer Query":

    st.title("New Customer Query")

    st.caption(
        "Submit a customer question to the TechNova AI support system."
    )

    customer_query = st.text_area(
        "Customer Question",
        placeholder="Example: What is your refund policy?",
        height=130
    )

    st.info(
        "Your question will be processed by Agent 01 first. "
        "Agent 02 will search the internet if internal information is insufficient."
    )

    if st.button("Submit Customer Query", type="primary"):

        if not customer_query.strip():

            st.warning("Please enter a customer question.")

        else:

            st.session_state["submitted_query"] = customer_query.strip()
            st.session_state["run_query"] = True

            st.rerun()

    if st.session_state.get("run_query", False):

        query = st.session_state["submitted_query"]

        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

        from crew import answer_customer

        with st.spinner(
            "AI agents are processing the customer question..."
        ):

            try:

                response = answer_customer(query)

                st.session_state["last_response"] = response
                st.session_state["run_query"] = False

                st.success("Customer query processed successfully.")

                st.subheader("Final Customer Support Response")
                st.write(response)

                st.info(
                    "The interaction has been submitted to the support log."
                )

            except Exception as error:

                st.session_state["run_query"] = False
                st.error(f"Unable to process the customer query: {error}")


# -----------------------------------
# TICKET HISTORY PAGE
# -----------------------------------

elif page == "Ticket History":

    st.title("Customer Ticket History")

    st.caption("Review previous customer interactions.")

    search_text = st.text_input(
        "Search tickets",
        placeholder="Search by customer question, agent or status..."
    )

    filtered_tickets = list(reversed(tickets))

    if search_text:

        filtered_tickets = [
            ticket for ticket in filtered_tickets
            if search_text.lower() in (
                ticket["customer"] + " "
                + ticket["agent"] + " "
                + ticket["status"]
            ).lower()
        ]

    st.write(f"Total matching tickets: {len(filtered_tickets)}")

    if filtered_tickets:

        for index, ticket in enumerate(filtered_tickets, start=1):

            with st.expander(
                f"Ticket {index}: {ticket['customer']}"
            ):

                st.write("**Date:**", ticket["date"])
                st.write("**Time:**", ticket["time"])
                st.write("**Answered By:**", ticket["agent"])
                st.write("**Status:**", ticket["status"])

                st.markdown("**Customer Support Response**")
                st.write(ticket["response"])

    else:
        st.info("No matching tickets found.")


# -----------------------------------
# KNOWLEDGE BASE PAGE
# -----------------------------------

elif page == "Knowledge Base":

    st.title("Company Knowledge Base")

    st.caption(
        "TechNova internal documents used by Agent 01."
    )

    if DATA_DIR.exists():

        documents = sorted(DATA_DIR.glob("*.txt"))

        if documents:

            for document in documents:

                with st.expander(document.name):

                    content = document.read_text(
                        encoding="utf-8"
                    )

                    st.write(content)

        else:

            st.warning("No company knowledge documents found.")

    else:

        st.error("Knowledge base directory not found.")


# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "TechNova Solutions | AI Customer Support Automation | Powered by CrewAI"
)
