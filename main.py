import uvicorn
import os

PORT = int(os.getenv("DBAPI_PORT", 8000))

if __name__ == "__main__":
    uvicorn.run("src.app.routes:app", host="0.0.0.0", port=PORT, reload=True)
