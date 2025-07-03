from uvicorn.config import Config
from uvicorn.server import Server
from fastapi.middleware.cors import CORSMiddleware
from main import app
from log.logger import logger


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def healthCheck():
    logger.info("Health check endpoint was called.")
    return "OK"


if __name__ == "__main__":
    port = 3015
    logger.debug(f"Starting server on http://localhost:{port}")
    config = Config(app=app, host="localhost", port=port)
    try:
        server = Server(config=config)
        server.run()
    except KeyboardInterrupt:
        logger.warning("Server stopped by user (KeyboardInterrupt).")
    except Exception as e:
        logger.exception(f"Error starting server: {e}")
        raise SystemExit(e)