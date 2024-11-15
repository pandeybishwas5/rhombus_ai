# rhombus_ai

Rhombus AI is a web application that allows users to upload CSV or Excel files, process them by inferring and converting data types, and display the cleaned data. It consists of a backend API built with Django and a frontend built with React.

Table of Contents
Backend Setup
Frontend Setup
File Upload API
License
Backend Setup (Django)
Clone the repository:

Clone the repository to your local machine.

bash
Copy code
git clone https://github.com/pandeybishwas5/rhombus_ai.git
cd rhombus_ai
cd backend
Create a virtual environment:

It's a good practice to use a virtual environment to manage dependencies.

Copy code
python -m venv venv
Activate the virtual environment:

On Windows:

Copy code
venv\Scripts\activate
On macOS/Linux:

bash
Copy code
source venv/bin/activate
Install dependencies:

Install the required Python packages listed in the requirements.txt file.

Copy code
pip install -r requirements.txt
Apply database migrations:

Run the following command to apply the database migrations.

Copy code
python manage.py migrate
Run the development server:

Start the Django backend server.

Copy code
python manage.py runserver
The backend API will be accessible at http://127.0.0.1:8000/.

Frontend Setup (React)
Navigate to the frontend directory:

The frontend is inside a separate directory within the project. Navigate to the frontend directory.

bash
Copy code
cd frontend
Install dependencies:

Make sure you have Node.js and npm installed. Then, run the following command to install the required dependencies for the frontend.

Copy code
npm install
Start the React development server:

Once dependencies are installed, start the React development server.

sql
Copy code
npm start
The frontend will be accessible at http://localhost:3000/.

