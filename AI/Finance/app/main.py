from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(
    title="Finance App",
    description=" Backend for analytics and trading research.",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Welcome to the Financial Portfolio API"}

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    os.chdir(r"C:\Users\nickc\Desktop\Code\Personal Projects\AI\Finance\app")
    # os.system("pwd")
    os.system(r'C:/Users/nickc/AppData/Local/Programs/Python/Python311/python.exe -m uvicorn main:app --reload')
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)