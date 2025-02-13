# Social Media Site - FastAPI Backend

## Overview

This is the backend of a social media site built using [FastAPI](https://fastapi.tiangolo.com/). It provides API endpoints for user authentication, post management, likes, comments, and other social media features.

## Features

- User authentication (signup, login)
- Post creation, deletion, and management
- Replies on posts
- Like, bookmark, and voting functionality for posts
- Support for image and poll attachments to posts
- Follower and following system
- User profile management

## Technologies Used

- **Framework**: FastAPI
- **Database**: SQLite
- **ORM**: SQLModel
- **Authentication**: JWT
- **Other Tools**: (Mention any other tools or libraries used, like Pydantic, etc.)

## Installation

### Prerequisites

- Python 3.13+ was installed on my system during development

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/osegbu/zentri.git
   cd <zentri>
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root of the project and add the following variables:

   ```ini
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=1440
   ```

5. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

   The app will be running at `http://127.0.0.1:8000`.

6. Check out the documentation and endpoints on:
   http://127.0.0.1:8000/docs.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss your ideas.

## Have A Feedback

Feel free to reach out to me!

Email: valentineosegbu@gmail.com
LinkedIn: https://www.linkedin.com/in/obinna-osegbu-746995174/
Twitter: @obinna_osegbu
GitHub Issues: You can also open an issue on this repository if it's related to the project.
