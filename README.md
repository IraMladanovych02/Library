# Library

Description
---
A project for efficient management the work of the library, 
providing convenient control of books, borrowings and users.

# Installation

### How to Set Up the Project

1. **Clone the Repository**  
   Fork the repository and clone it to your local machine:
   ```bash
   git clone https://github.com/YOUR-USERNAME/Library.git
   ```

2. **Set Up a Virtual Environment**  
   Create a virtual environment and activate it. Then, install the required dependencies:
   
   - On **Windows**:
     ```bash
     python -m venv venv
     venv\Scripts\activate
     pip install -r requirements.txt
     ```
   
   - On **macOS/Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

3. **Create a Superuser**  
   To manage the project through the admin panel, create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run the Development Server**  
   Start the server to check if the website is running:
   ```bash
   python manage.py runserver
   ```

---

# Features

• JWT authenticated

• Admin panel /admin/

• Managing books, borrowing, users

• Telegram bot notifications
