from waitress import serve
from app import create_app

if __name__ == "__main__":
    app = create_app()
    print("Starting server on port 8080 with 8 threads...")
    serve(app, host='localhost', port=8080, threads=4, backlog=2048, connection_limit=500)
