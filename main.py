import os
from retriever import ask_question

def main():
    print("\n" + "="*50)
    print("📚 Document Q&A Bot - Command Line Version")
    print("="*50)
    
    if not os.path.exists("./vectorstore") or not os.listdir("./vectorstore"):
        print("\n❌ No index found!")
        print("Please run: python ingest.py first")
        return
    
    print("\n✅ Bot is ready! Type your question.")
    print("Type 'exit' to quit.\n")
    
    while True:
        question = input("You: ").strip()
        
        if not question:
            continue
            
        if question.lower() == "exit":
            print("Goodbye! 👋")
            break
        
        print("\n🤔 Thinking...")
        
        try:
            answer, sources = ask_question(question)
            print(f"\n🤖 Answer:\n{answer}")
            
            if sources:
                print("\n📚 Sources:")
                for source in sources:
                    print(f"  {source}")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    main()