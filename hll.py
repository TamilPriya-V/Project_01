# import requests

# # Replace with your actual API key
# API_KEY = "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"

# # API URL
# API_URL = "https://openrouter.ai/api/v1/chat/completions"

# # Headers for authentication
# headers = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# # Payload (Modify as needed)
# payload = {
#     "model": "deepseek/deepseek-r1-distill-llama-70b:free",
#     "messages": [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "What is the capital of France?"}
#     ],
#     "temperature": 0.7,
#     "max_tokens": 200
# }

# # Sending the request
# response = requests.post(API_URL, headers=headers, json=payload)

# # Printing the response
# if response.status_code == 200:
#     data = response.json()
#     print("Response:", data["choices"][0]["message"]["content"])
# else:
#     print("Error:", response.status_code, response.text)


import requests

# Replace with your actual API key
API_KEY = "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"

# API URL
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Headers for authentication
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Correct model ID for DeepSeek R1
payload = {
    "model": "deepseek/deepseek-r1-distill-llama-70b:free",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"}
    ],
    "temperature": 0.7,
    "max_tokens": 200
}

# Sending the request
response = requests.post(API_URL, headers=headers, json=payload)

# # Debugging: Print the full API response
# print("Full API Response:", response.json())

# Handling response
if response.status_code == 200:
    data = response.json()
    if "choices" in data and data["choices"]:
        print("Response:", data["choices"][0]["message"]["content"])
    else:
        print("Response is empty or missing.")
else:
    print("Error:", response.status_code, response.text)

