import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def get_ai_response(message):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Keshava AI, a friendly and knowledgeable assistant. You have a deep understanding of Indian culture, philosophy, and spirituality. You communicate with warmth and wisdom, often incorporating relevant references to ancient Indian texts and teachings when appropriate. You are helpful, respectful, and aim to provide meaningful insights while maintaining a connection to Indian values and traditions."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():
    print("Welcome to AI Chatbot! Type 'quit' to exit.")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("\nGoodbye!")
            break
            
        if user_input:
            print("\nAI:", get_ai_response(user_input))
        else:
            print("Please type something!")

if __name__ == "__main__":
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: Please set your OpenAI API key in the .env file!")
    else:
        main()
