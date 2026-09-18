# 🏨 Hotel AI Assistant

A modern AI-powered hotel concierge chatbot built using **Streamlit, Python, Google Gemini API, and a JSON-based hotel knowledge base**.

The assistant helps hotel guests get quick and polite answers about hotel facilities, check-in/check-out timings, breakfast, parking, spa, gym, dining, and other hotel-related services.

---

## ✨ Features

* AI-powered hotel customer support chatbot
* Modern luxury black and red user interface
* Built with Streamlit
* Google Gemini API integration
* JSON-based hotel knowledge base
* Context-aware chat session
* Suggested questions for common hotel queries
* Friendly and polite responses
* Restricts answers to available hotel information
* Responsive interface for desktop and mobile
* Chat history maintained during the session
* Secure API key management using environment variables

---

## 🛠️ Tech Stack

### Frontend

* Streamlit
* HTML
* CSS
* Custom responsive styling
* Streamlit chat components

### Backend

* Python
* Google GenAI SDK
* Gemini Flash model
* Session state management
* JSON knowledge base

### Data Storage

* `hotel_data.json`
* Stores hotel-related information used by the chatbot

### API Integration

* Google Gemini API
* API key loaded through environment variables

---

## 🏗️ Project Architecture

```text
User
  │
  ▼
Streamlit Frontend
  │
  │ User enters a question
  ▼
Python Application Logic
  │
  ▼
Hotel Knowledge Base
(hotel_data.json)
  │
  ▼
System Prompt + User Query
  │
  ▼
Google Gemini API
  │
  ▼
AI-generated Response
  │
  ▼
Streamlit Chat Interface
```

---

## 📁 Project Structure

```text
Hotel_Chatbot/
│
├── Hotel_Chatbot.py       # Main Streamlit application
├── hotel_data.json        # Hotel knowledge base
├── .env                   # API key configuration
├── .gitignore             # Prevents sensitive files from being committed
└── README.md              # Project documentation
```

---

## 🎨 Frontend

The frontend is developed using **Streamlit**.

It provides a conversational interface where users can:

* Enter hotel-related questions
* View previous messages
* Use suggested questions
* Receive AI-generated responses
* Interact with a clean chat-based layout

### UI Design

The interface uses a premium hotel-inspired design with:

* Black background
* Luxury red accent colors
* Rounded chat containers
* Glassmorphism-style input box
* Responsive layout
* Custom typography
* Hover effects
* Hotel concierge branding

Example suggested questions include:

```text
Is breakfast included?
What time is check-in and check-out?
Do you have a gym or spa?
Is parking available on-site?
```

---

## ⚙️ Backend

The backend logic is implemented in Python inside `Hotel_Chatbot.py`.

The backend is responsible for:

1. Loading environment variables
2. Reading the hotel knowledge base
3. Creating the AI system prompt
4. Initializing the Gemini client
5. Maintaining the chat session
6. Sending user queries to Gemini
7. Displaying the generated response
8. Maintaining chat history

The application uses Streamlit session state to preserve:

* Gemini client
* Gemini chat session
* User messages
* Assistant responses

---

## 🧠 Knowledge Base

The chatbot uses a local JSON file named:

```text
hotel_data.json
```

This file contains the hotel's information, such as:

* Hotel facilities
* Room information
* Breakfast details
* Check-in and check-out timings
* Parking availability
* Gym and spa details
* Dining information
* Hotel policies
* Guest services

The JSON data is loaded into the application and included in the system prompt sent to Gemini.

This allows the chatbot to answer based on the hotel's actual information rather than generating unrelated answers.

---

## 🤖 AI Integration

The chatbot uses the **Google Gemini API** through the Google GenAI Python SDK.

The Gemini model is initialized using:

```python
from google import genai
```

The API key is loaded from an environment variable:

```python
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
```

The Gemini client is created using:

```python
genai.Client(api_key=GOOGLE_API_KEY)
```

A chat session is then created with a system instruction containing the hotel knowledge base.

```python
st.session_state.chat = st.session_state.client.chats.create(
    model="gemini-3.6-flash",
    config={"system_instruction": prompt},
)
```

When the user submits a question, it is sent to Gemini:

```python
response = st.session_state.chat.send_message(user_input)
```

The generated response is displayed in the Streamlit interface.

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

Never upload your API key to GitHub or expose it publicly.

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Dhanusiya-B/Hotel_Chatbot.git
cd Hotel_Chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install streamlit google-genai python-dotenv
```

### 5. Configure the API Key

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 6. Run the Application

```bash
streamlit run Hotel_Chatbot.py
```

The application will open in your browser at:

```text
http://localhost:8501
```

---

## 💬 Application Workflow

1. The user opens the hotel chatbot.
2. The Streamlit frontend displays the welcome screen.
3. The user types a question or selects a suggested question.
4. The application reads the hotel knowledge base.
5. The question and hotel information are passed to Gemini.
6. Gemini generates a polite response.
7. The response is displayed in the chat interface.
8. The conversation is maintained using Streamlit session state.

---

## 🧩 Prompt-Based Response Control

The chatbot is instructed to behave as a hotel customer care executive.

Its response rules include:

* Respond politely and professionally
* Answer only using the hotel knowledge base
* Avoid inventing hotel information
* Clearly state when information is unavailable
* Provide helpful and guest-friendly responses

This improves response accuracy and prevents unsupported answers.

---

## 📌 Example Queries

Users can ask:

```text
Is breakfast included in the room booking?
What time is check-in?
What time is check-out?
Is parking available?
Does the hotel have a gym?
Do you provide spa services?
What dining options are available?
```

---

## 🔮 Future Enhancements

* Booking and reservation integration
* Live room availability
* Database integration using MySQL
* Admin dashboard
* Guest authentication
* Multilingual chatbot support
* Voice-based hotel assistant
* WhatsApp integration
* Email notification system
* Retrieval-Augmented Generation (RAG)
* Conversation analytics
* Deployment using Streamlit Cloud
* Integration with hotel management systems

---

## 🌐 Deployment

The application can be deployed using platforms such as:

* Streamlit Community Cloud
* LIVE DEMO LINK: https://hfwbg8cdwz65g5gsubkgyr.streamlit.app/

For deployment, configure the Gemini API key using the platform's secret/environment variable settings instead of uploading the `.env` file.

---

## 👩‍💻 Author

**Dhanusiya B.**

Computer Science and Engineering Graduate

GitHub:
https://github.com/Dhanusiya-B

LinkedIn:
https://www.linkedin.com/in/dhanusiyab

---

## 📄 License

This project is created for educational, portfolio, and demonstration purposes.
