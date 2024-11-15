# rhombus_ai

Rhombus AI is a web application that allows users to upload CSV or Excel files, process them by inferring and converting data types, and display the cleaned data. It consists of a backend API built with Django and a frontend built with React.

Backend Setup (Django)

Clone the repository:

Clone the repository to your local machine.
-- git clone https://github.com/pandeybishwas5/rhombus_ai.git
-- cd rhombus_ai
-- cd backend

Insall Dependencied

-- pip install -r requirements.txt


Apply database migrations:

Run the following command to apply the database migrations.

-- python manage.py migrate


Run the development server:

Start the Django backend server.
-- python manage.py runserver
The backend API will be accessible at http://127.0.0.1:8000/.

Frontend Setup (React)
Navigate to the frontend directory:

The frontend is inside a separate directory within the project. Navigate to the frontend directory.

-- cd frontend


Install dependencies:

Make sure you have Node.js and npm installed. Then, run the following command to install the required dependencies for the frontend.

-- npm install


Start the React development server:

Once dependencies are installed, start the React development server.

-- npm run dev


The frontend will be accessible at http://localhost:5137/.

