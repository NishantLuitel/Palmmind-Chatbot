"""
This module runs the chatbot and you can interact via command prompt
"""



if __name__== "__main__":
    from chat_agent import ChatAgent
    c = input("Which specialization chatbot? Cell biology(press 'c') or Neurology(press 'n') or Custom(press 'p')?:")

    if c == 'c':
        ca = ChatAgent()
    elif c == 'n':
        ca = ChatAgent(specialize = 'psichiatry')
    elif c=='p':
        name = input("Enter pdf file name: ")
        ca = ChatAgent(specialize = 'custom',custom_file=name)
    
    print("\nAsk a question to your AI assistant!")
    print("Enter 'End' to exit the conversation.")
    while(True):
        input_text = input("You: ")
        if input_text == 'End':
            break
        reply_msg = ca.reply(input_text)
        print("AI:", reply_msg)


    


