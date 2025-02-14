# Zentri - A Social Media Site - FastAPI Backend

This is the **backend** of Zentri, providing API endpoints for user authentication, post management, likes, comments, and other social media features.

## Getting Started

### Prerequisites

- Python 3.13+ was installed on my system during development

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/osegbu/zentri-backend.git
   cd zentri-backend
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

## Frontend Repository

The frontend for this project is built using **Next.js**. You can find the repository for the frontend [here](https://github.com/osegbu/zentri-nexjs).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss your ideas.

## Have A Feedback?

Feel free to reach out to me!

- **Email**: [valentineosegbu@gmail.com](mailto:valentineosegbu@gmail.com)
- **LinkedIn**: [Obinna Osegbu](https://www.linkedin.com/in/obinna-osegbu-4aa304200/)
- **Twitter**: [@obinna_osegbu](https://twitter.com/obinna_osegbu)
- **GitHub Issues**: You can also open an issue on this repository if it's related to the project.
