# Trades Engine: AI-Powered Market Analyzer

A full-stack, containerized algorithmic trading dashboard. This system fetches live stock market data, processes it through a background AI engine, and serves Buy/Sell/Hold signals to a clean, isolated user interface.

---

## 🧠 The Architecture: What is What?

This project is broken down into two main parts: the custom logic (my code) and the infrastructure (the heavy lifters).

### 1. My Custom Application (The Logic)
This is the code I wrote to make the platform unique:
* **The Trading Floor UI (`index.html`):** A custom Bootstrap 5 dashboard that displays live market prices, user portfolios, and real-time order execution logs.
* **The AI Dashboard:** A secondary, isolated UI that asynchronously fetches the latest AI recommendations using vanilla JavaScript `fetch()` calls.
* **The AI Engine (`utils.py`):** The core Python logic that connects to Yahoo Finance, downloads 30 days of historical closing prices, formats the data, and explicitly prompts the Groq Llama 3.1 LLM to act as a financial analyst.
* **The Data Models (`models.py`):** The custom database schema tracking `Assets` (tickers), user `Portfolios`, order histories, and the AI `Signals`.

### 2. The Infrastructure (The Engines)
These are the powerful open-source tools running behind the scenes to make the system scalable:
* **Django:** The core Python web framework handling HTTP routing, database connections, and secure admin authentication.
* **Redis:** The in-memory message broker. It acts as a high-speed waiting room, holding tasks until the background workers are ready for them.
* **Celery & Celery Beat:** The asynchronous task managers. `Beat` watches the clock and schedules the AI updates, while the `Worker` physically executes the API calls in the background so the main website never slows down.
* **Groq LPU:** The insanely fast AI inference engine running the `llama-3.1-8b-instant` model to analyze the stock trends.
* **Docker Compose:** The containerization system that bundles the entire ecosystem (Server, Worker, Scheduler, and Redis) into a single command.

---

## 🚀 How to Run the System

Because the entire architecture is containerized, you do not need to open multiple terminals or install Redis locally.

### 1. Set Your Credentials
Create a `.env` file in the root directory and add your Groq API key.