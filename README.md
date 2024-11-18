# Project Name

## Description

This project is a terminal chat application that allows users to register, login, and interact with the application. It provides a simple and intuitive interface for communication.

## Installation

To run this project, follow these steps:

1. Open your terminal and navigate to the `terminal-chat` folder using the `cd` command.
2. Create a virtual environment using the command `virtualenv venv`.
3. Activate the virtual environment with the command `source venv/bin/activate` (for Linux/Mac) or `venv\Scripts\activate` (for Windows).
4. Install the project dependencies by running `pip install -r requirements.txt`.
5. Run the necessary migrations using Alembic by executing `alembic upgrade head`.
6. Start the server by running `uvicorn app.main:app` in your terminal.
7. Open two additional terminal instances and run `python main.py` in both instances.
8. Register or login to start using the application.

## Future Plans

Although the feature for group chat was not implemented due to time constraints, the current implementation provides a solid foundation for future development. Here are some points about the implementation and future plans:

- The application was implemented using Python and the FastAPI framework for its simplicity and performance.
- The database management is handled by Alembic, which allows for easy migration of database schemas.
- In the future, the group chat feature can be implemented by extending the existing functionality and adding appropriate endpoints and database models.
- Additional features such as message encryption, file sharing, and user profiles can also be considered for future development.

Feel free to explore and contribute to this project!
