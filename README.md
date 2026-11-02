# TechNova — AI Customer Support Automation

An intelligent customer support automation system built using **CrewAI, Retrieval-Augmented Generation (RAG), OpenAI, FAISS, and Streamlit**.

The system uses three specialized AI agents to answer customer questions using internal company documents, research the internet when internal information is insufficient, and maintain a customer interaction history.

## Project Overview

TechNova Solutions is a fictional technology company. This project demonstrates how multiple AI agents can collaborate to automate customer support operations.

### AI Agents

**1. RAG Customer Support Agent**

- Understands customer questions.
- Searches the company's internal knowledge base.
- Uses FAISS vector search and OpenAI embeddings.
- Provides answers based on company documents.
- Returns `INTERNAL_KB_INSUFFICIENT` when the available internal information cannot answer the question.

**2. Internet Research Agent**

- Receives questions that require external information.
- Searches the internet using the DDGS search library.
- Retrieves relevant articles and information.
- Provides headlines, sources, publication dates, descriptions, and URLs when available.
- Does not present general internet information as official company policy.

**3. Customer Support Log Agent**

- Records every customer interaction.
- Stores the customer question and final response.
- Records the answering agent, date, time, and status.
- Appends records to a local text file for future reference.

## Dashboard

The project includes a Streamlit web dashboard for interacting with the customer support system.

Dashboard features:

- Overview of customer support activity.
- Total ticket statistics.
- Resolved ticket count.
- External research count.
- Pending confirmation count.
- Customer query submission.
- Ticket history.
- Knowledge base navigation.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| CrewAI | Multi-agent orchestration |
| OpenAI | AI language model |
| LangChain | Document processing |
| FAISS | Vector database and similarity search |
| OpenAI Embeddings | Document embeddings |
| DDGS | Internet search |
| Streamlit | Web dashboard |
| Python-dotenv | Environment variable management |

## Project Structure

```text
customer-support-crewai/
│
├── agents/
│   ├── __init__.py
│   ├── rag_agent.py
│   ├── web_agent.py
│   └── log_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── rag_tool.py
│   └── web_search_tool.py
│
├── data/
│   ├── company_info.txt
│   ├── refund_policy.txt
│   ├── shipping_policy.txt
│   └── product_faq.txt
│
├── logs/
│   └── customer_support_history.txt
│
├── knowledge_base/
│   └── faiss_index/
│
├── config/
│   └── settings.py
│
├── dashboard/
│   ├── __init__.py
│   └── dashboard.py
│
├── main.py
├── crew.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```cmd
git clone YOUR_GITHUB_REPOSITORY_URL
cd customer-support-crewai
```

### 2. Create a virtual environment

```cmd
python -m venv venv
```

### 3. Activate the environment

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```cmd
pip install -r requirements.txt
```

### 5. Configure the OpenAI API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Replace the placeholder with your own OpenAI API key.

**Important:** Never upload your actual `.env` file or API key to GitHub.

### 6. Run the application

To start the command-line application:

```cmd
python main.py
```

To launch the Streamlit dashboard:

```cmd
streamlit run dashboard\dashboard.py
```

Open the local dashboard in your browser:

```text
http://localhost:8501
```

## Example Customer Queries

**Example 1 — Internal Knowledge Base**

Question:

> I purchased a laptop 3 days ago. It is unused and in its original packaging. Can I return it?

Expected behaviour: The RAG Customer Support Agent searches the internal refund policy and provides an answer.

**Example 2 — Company Policy Confirmation**

Question:

> Does TechNova deliver products to the United States?

Expected behaviour: The system checks internal shipping information and explains that international shipping is not officially confirmed.

**Example 3 — Internet Research**

Question:

> What are the latest AI technology news updates today?

Expected behaviour: The Internet Research Agent searches for relevant current news and provides available headlines, sources, publication dates, and URLs.

## Customer Interaction Logging

All customer interactions are appended to:

```text
logs/customer_support_history.txt
```

The log stores:

- Customer question
- Final response
- Answering agent
- Date and time
- Ticket status

This history can be used for future reference and customer support monitoring.

## Security

- API keys are stored in environment variables.
- `.env` is excluded from Git tracking.
- `.env.example` provides a placeholder configuration.
- Customer interaction logs are maintained locally.

## Future Improvements

- Advanced ticket search and filtering.
- Human review and approval workflow.
- Customer feedback and satisfaction tracking.
- Export ticket history to Excel.
- Improved analytics and reporting.
- Deployment to a cloud hosting platform.

## Project Objective

The objective of this project is to demonstrate how multiple specialized AI agents can work together to automate customer support using internal knowledge retrieval, external internet research, and interaction logging through a user-friendly web dashboard.

---

**Developed as an AI Agent Automation Project using CrewAI and Python.**
