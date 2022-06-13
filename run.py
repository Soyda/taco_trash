
from API import main
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app")