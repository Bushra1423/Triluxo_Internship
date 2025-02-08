import requests

def main():
    api_url = "http://127.0.0.1:5000/chat"
    user_input = input("Ask a question to the chatbot: ")
    payload = {"question": user_input}
    
    # Make the POST request
    response = requests.post(api_url, json=payload)
    
    # Print status code and response text for debugging
    print("Status Code:", response.status_code)
    
    
    if response.status_code == 200:
        try:
            data = response.json()
            print("Chatbot Response:", data.get("response"))
        except Exception as e:
            print("Error parsing JSON:", e)
    else:
        print("Error response:", response.text)

if __name__ == "__main__":
    main()
