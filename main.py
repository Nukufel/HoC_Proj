from agent import agent, invoke_agent

def main():
    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        result = invoke_agent(user_input)

        # last assistant message
        response = result["messages"][-1].content

        print(f"\nAssistant: {response}\n")

if __name__ == "__main__":
    main()