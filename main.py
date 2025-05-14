from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# Store WebSocket connections
connected_clients = []

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()  # keep the connection alive
    except:
        connected_clients.remove(websocket)

@app.post("/test_postback")
async def test_postback(request: Request):
    data = await request.json()
    # Send message to all connected clients
    for ws in connected_clients:
        await ws.send_text(f"Postback received with data: {data}")
    return {"status": "ok"}
