from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
from typing import List, Dict, Any

class ConnectionManager:
    """WebSocket连接管理器"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        """建立新的WebSocket连接"""
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        """关闭WebSocket连接"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
    
    async def send_json(self, websocket: WebSocket, data: Dict[str, Any]):
        """向指定的WebSocket连接发送JSON数据"""
        await websocket.send_json(data)
    
    async def broadcast_json(self, data: Dict[str, Any]):
        """向所有活跃的WebSocket连接广播JSON数据"""
        for connection in self.active_connections:
            await connection.send_json(data)

# 创建连接管理器实例
manager = ConnectionManager()