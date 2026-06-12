import uvicorn


def run() -> None:
    uvicorn.run("final_orders.app:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    run()
