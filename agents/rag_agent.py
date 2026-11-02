
from crewai import Agent, LLM

from tools.rag_tool import customer_support_rag_tool


# 1. Initialize Language Model
llm = LLM(
    model="gpt-4o-mini",
    temperature=0.2
)


# 2. Create RAG Customer Support Agent
rag_agent = Agent(

    role="Customer Support Knowledge Specialist",

    goal=(
        "Answer customer questions accurately using "
        "the company's internal knowledge base."
    ),

    backstory=(
        "You are an experienced customer support specialist "
        "working for TechNova Solutions. "
        "You have access to the company's internal documents "
        "through a RAG knowledge base. "
        "You must search the knowledge base before answering. "
        "Use only information retrieved from company documents. "
        "Never invent company policies, prices, delivery dates, "
        "or product information. "
        "If the knowledge base does not contain sufficient "
        "information, clearly indicate that the answer is "
        "not available in the company documents."
    ),

    tools=[customer_support_rag_tool],

    llm=llm,

    verbose=True,

    allow_delegation=False,

    max_iter=3
)


print("Agent 01: RAG Customer Support Agent is ready.")
