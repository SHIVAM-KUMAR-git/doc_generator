# DOC Report Generator

A Python application that automates the process of fetching user data from an API and generating a formatted text report. 
This project serves as a practical example of **Object-Oriented Programming (OOP)**, **API Integration**, and **Robust Error Handling** in Python.

## 📋 Features
*   **Automated Data Fetching**: Retrieves data from `jsonplaceholder.typicode.com`.
*   **OOP Architecture**: Built using classes (`ApiClient`, `UserData`, `ReportGenerator`) for clean, maintainable code.
*   **Custom Error Handling**: Gracefully handles network issues and data parsing errors.
*   **File Generation**: Automatically creates a structured text report with a timestamp.

## 🚀 Getting Started

### Prerequisites
*   Python 3.x installed.
*   The `requests` library.

### Installation
1.  Install the required dependency:
    ```bash
    pip install requests
    ```

### How to Run
1.  Execute the script in your terminal:
    ```bash
    python doc_generator.py
    ```
2.  The script will:
    *   Fetch data from the API.
    *   Print status messages to the console.
    *   Generate a report file in the `generated_reports/` directory.

## 🛠️ Technical Concepts
This single-module script (`doc_generator.py`) demonstrates:
*   **Encapsulation**: Using `dataclasses` to model User entities.
*   **Abstraction**: Separating API logic into a dedicated `ApiClient` class.
*   **Exception Handling**: Implementing custom exceptions (`APIConnectionError`, `DataParseError`) for reliable execution.
*   **f-strings**: Using modern Python string formatting for the report output.

