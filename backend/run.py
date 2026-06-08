import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="34.131.129.112/mcp",
        # port=8000,
        reload=True
    )