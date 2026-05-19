# import os
# from dotenv import load_dotenv

# load_dotenv()

# from app.schemas.chat_schema import ChatMessage
# from app.services.chat_service import ChatService

# def main():
#     print("Starting ChatService test...")
    
#     api_key = os.getenv("GEMINI_API_KEY")
#     if not api_key:
#         print("ERROR: GEMINI_API_KEY is not set in your .env file.")
#         return
        
#     print(f"Loaded API key successfully. Prefix: {api_key[:8]}...")
    
#     print("\n--- Test 1: Simple chat with no history ---")
#     message = "Tell me a very short one-sentence joke about programming."
#     try:
#         response = ChatService.generate_chat_response(
#             message=message,
#             history=[],
#             model="gemini-2.5-flash",
#             temperature=0.7,
#             api_key=api_key
#         )
#         print(f"User: {message}")
#         print(f"Assistant ({response.model}): {response.response}")
#     except Exception as e:
#         print(f"Test 1 FAILED: {str(e)}")

#     print("\n--- Test 2: Chat with conversation history ---")
#     history = [
#         ChatMessage(role="user", content="Hello, I am Antigravity. I love AI coding."),
#         ChatMessage(role="assistant", content="Hello Antigravity! That sounds fantastic. How can I help you today?")
#     ]
#     message = "What was my name again and what do I love?"
#     try:
#         response = ChatService.generate_chat_response(
#             message=message,
#             history=history,
#             model="gemini-2.5-flash",
#             temperature=0.7,
#             api_key=api_key
#         )
#         print(f"User: {message}")
#         print(f"Assistant ({response.model}): {response.response}")
#     except Exception as e:
#         print(f"Test 2 FAILED: {str(e)}")

# if __name__ == "__main__":
#     main()
