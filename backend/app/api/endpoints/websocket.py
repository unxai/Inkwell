from fastapi import WebSocket, WebSocketDisconnect
import json
import asyncio
import time
import uuid
from typing import List, Dict, Any, Optional
from app.core.logger import logger

class ConnectionManager:
    """WebSocket连接管理器，支持连接超时和心跳机制"""
    
    def __init__(self, heartbeat_interval: int = 30, connection_timeout: int = 300):
        """
        初始化WebSocket连接管理器
        
        参数:
        - heartbeat_interval: 心跳间隔（秒）
        - connection_timeout: 连接超时时间（秒）
        """
        self.active_connections: Dict[str, Dict[str, Any]] = {}
        self.heartbeat_interval = heartbeat_interval
        self.connection_timeout = connection_timeout
        self.heartbeat_task = None
    
    async def connect(self, websocket: WebSocket):
        """建立新的WebSocket连接"""
        await websocket.accept()
        
        # 生成唯一的连接ID
        connection_id = str(uuid.uuid4())
        
        # 存储连接信息
        self.active_connections[connection_id] = {
            "websocket": websocket,
            "last_activity": time.time(),
            "connection_id": connection_id
        }
        
        # 记录连接建立
        logger.info({
            "message": "WebSocket连接已建立",
            "connection_id": connection_id,
            "active_connections": len(self.active_connections)
        })
        
        # 启动心跳检查任务（如果尚未启动）
        if self.heartbeat_task is None or self.heartbeat_task.done():
            self.heartbeat_task = asyncio.create_task(self._heartbeat_check())
        
        return connection_id
    
    def disconnect(self, websocket: WebSocket):
        """关闭WebSocket连接"""
        # 查找并移除连接
        connection_id = None
        for conn_id, conn_info in list(self.active_connections.items()):
            if conn_info["websocket"] == websocket:
                connection_id = conn_id
                del self.active_connections[conn_id]
                break
        
        # 记录连接关闭
        if connection_id:
            logger.info({
                "message": "WebSocket连接已关闭",
                "connection_id": connection_id,
                "active_connections": len(self.active_connections)
            })
    
    def update_activity(self, websocket: WebSocket):
        """更新连接的最后活动时间"""
        for conn_info in self.active_connections.values():
            if conn_info["websocket"] == websocket:
                conn_info["last_activity"] = time.time()
                break
    
    async def send_json(self, websocket: WebSocket, data: Dict[str, Any]):
        """向指定的WebSocket连接发送JSON数据"""
        try:
            await websocket.send_json(data)
            self.update_activity(websocket)
        except Exception as e:
            logger.error({
                "message": "发送WebSocket消息失败",
                "error": str(e)
            })
            # 尝试断开连接
            self.disconnect(websocket)
    
    async def broadcast_json(self, data: Dict[str, Any]):
        """向所有活跃的WebSocket连接广播JSON数据"""
        for conn_info in list(self.active_connections.values()):
            try:
                await conn_info["websocket"].send_json(data)
                self.update_activity(conn_info["websocket"])
            except Exception as e:
                logger.error({
                    "message": "广播WebSocket消息失败",
                    "connection_id": conn_info["connection_id"],
                    "error": str(e)
                })
                # 尝试断开连接
                self.disconnect(conn_info["websocket"])
    
    async def send_heartbeat(self, websocket: WebSocket):
        """发送心跳消息"""
        try:
            await websocket.send_json({"type": "heartbeat", "timestamp": time.time()})
            self.update_activity(websocket)
            return True
        except Exception as e:
            logger.error({
                "message": "发送心跳消息失败",
                "error": str(e)
            })
            return False
    
    async def _heartbeat_check(self):
        """定期检查连接状态并发送心跳"""
        try:
            while True:
                current_time = time.time()
                
                # 检查所有连接
                for conn_id, conn_info in list(self.active_connections.items()):
                    last_activity = conn_info["last_activity"]
                    websocket = conn_info["websocket"]
                    
                    # 检查是否超时
                    if current_time - last_activity > self.connection_timeout:
                        logger.info({
                            "message": "WebSocket连接超时",
                            "connection_id": conn_id,
                            "inactive_seconds": int(current_time - last_activity)
                        })
                        self.disconnect(websocket)
                        continue
                    
                    # 如果接近心跳间隔，发送心跳
                    if current_time - last_activity > self.heartbeat_interval * 0.8:
                        success = await self.send_heartbeat(websocket)
                        if not success:
                            self.disconnect(websocket)
                
                # 等待下一次检查
                await asyncio.sleep(self.heartbeat_interval / 2)
                
        except asyncio.CancelledError:
            logger.info({"message": "心跳检查任务已取消"})
        except Exception as e:
            logger.error({
                "message": "心跳检查任务出错",
                "error": str(e)
            })

# 创建连接管理器实例
manager = ConnectionManager()
