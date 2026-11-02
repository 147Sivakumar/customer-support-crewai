
from crew import answer_customer


def main():

    print("\n========================================")
    print("   TECHNOVA CUSTOMER SUPPORT SYSTEM")
    print("========================================")

    print("\nAsk your question.")
    print("Type 'exit' to close the application.")

    while True:

        customer_query = input("\nCustomer: ").strip()

        if customer_query.lower() in ["exit", "quit"]:

            print("\nThank you for contacting TechNova Support!")
            break

        if not customer_query:

            print("Please enter a valid question.")
            continue

        try:

            answer_customer(customer_query)

        except Exception as error:

            print("\nUnable to process your request.")
            print("Error:", error)


if __name__ == "__main__":
    main()
