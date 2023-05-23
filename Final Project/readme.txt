 Enter your project directory

-----------------cd #project-path

2) Install Pipenv
---------------pip install pipenv
3) Install the dependencies
---------------pipenv install
4) Enter the pipenv virtual environment
---------------pipenv shell

5) run the program files present in the project

6)Build your image
docker build -t customer_churn .

7)Run the app
docker run -d -p 8501:8501 customer_churn