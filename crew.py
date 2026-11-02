
from crewai import Crew, Task, Process

from agents.rag_agent import rag_agent
from agents.web_agent import web_agent
from agents.log_agent import save_customer_interaction


# Marker used to trigger internet fallback
FALLBACK_MARKER = "INTERNAL_KB_INSUFFICIENT"


def answer_customer(customer_query: str):

    print("\n" + "=" * 50)
    print("CUSTOMER SUPPORT WORKFLOW STARTED")
    print("=" * 50)

    # Default values
    answered_by = "Agent 01 - RAG Agent"
    status = "Answered"

    # ---------------------------------
    # STEP 1: Agent 01 - Search RAG
    # ---------------------------------

    print("\n[Agent 01] Searching company knowledge base...")

    rag_task = Task(

        description=f"""
        Customer Question:
        {customer_query}

        Instructions:

        1. Search the internal company knowledge base
           using the RAG tool.

        2. Answer only using relevant company documents.

        3. If sufficient information is available,
           provide a clear and professional answer.

        4. If the company documents do not contain
           sufficient information to answer the question,
           return exactly this marker:

           {FALLBACK_MARKER}

        Do not invent company policies or information.
        """,

        expected_output=(
            "A company-document-based answer, or exactly "
            f"{FALLBACK_MARKER} when information is insufficient."
        ),

        agent=rag_agent
    )

    rag_crew = Crew(
        agents=[rag_agent],
        tasks=[rag_task],
        process=Process.sequential,
        verbose=True
    )

    rag_result = rag_crew.kickoff()

    response = str(rag_result).strip()

    # ---------------------------------
    # STEP 2: Agent 02 - Internet Search
    # ---------------------------------

    if FALLBACK_MARKER in response.upper():

        print("\n[Agent 01] Internal information insufficient.")

        print("\n[Agent 02] Searching the internet...")

        answered_by = "Agent 02 - Internet Research Agent"
        status = "External Research - Verify Company Details"

        web_task = Task(

            description=f"""
            Customer Question:
            {customer_query}

            The internal company knowledge base could not
            provide sufficient information.

            Instructions:

            1. Use the Internet Search Tool.
            2. Search for relevant and reliable information.
            3. Prefer authoritative sources.
            4. Prepare a clear and professional answer.
            5. Include the source URLs.
            6. Never invent facts or URLs.
            7. Never present general internet information
               as official TechNova company policy.
            8. If the answer requires company confirmation,
               clearly mention that.

            If no reliable information is found or search
            fails, explain that the answer could not
            be verified.
            """,

            expected_output=(
                "A researched answer with source URLs, "
                "or a clear explanation that information "
                "could not be verified."
            ),

            agent=web_agent
        )

        web_crew = Crew(
            agents=[web_agent],
            tasks=[web_task],
            process=Process.sequential,
            verbose=True
        )

        web_result = web_crew.kickoff()

        response = str(web_result).strip()

    # ---------------------------------
    # STEP 3: Agent 03 - Save Interaction
    # ---------------------------------

    print("\n[Agent 03] Saving customer interaction...")

    try:

        log_file = save_customer_interaction(
            customer_query=customer_query,
            agent_response=response,
            answered_by=answered_by,
            status=status
        )

        print(f"Log saved: {log_file}")

    except Exception as error:

        print(f"WARNING: Logging failed: {error}")

    # ---------------------------------
    # STEP 4: Return Final Answer
    # ---------------------------------

    print("\n" + "=" * 50)
    print("FINAL CUSTOMER SUPPORT RESPONSE")
    print("=" * 50)

    print(response)

    print("\nAnswered By:", answered_by)
    print("Status:", status)

    return response


if __name__ == "__main__":

    query = input("\nCustomer Query: ")

    answer_customer(query)
