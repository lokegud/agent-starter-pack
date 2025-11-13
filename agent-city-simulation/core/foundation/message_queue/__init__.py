"""Message queue foundation for Agent City Simulation."""

from .kafka_client import MessageQueueManager, get_message_queue

__all__ = ["MessageQueueManager", "get_message_queue"]
