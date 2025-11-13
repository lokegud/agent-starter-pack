"""
Kafka message queue management.

Provides pub/sub messaging for inter-service communication.
"""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from aiokafka.errors import KafkaError

from core.shared.config import get_settings

logger = logging.getLogger(__name__)


class MessageQueueManager:
    """Manages Kafka message queue connections and operations."""

    def __init__(self):
        """Initialize message queue manager."""
        self.settings = get_settings()
        self._producer: Optional[AIOKafkaProducer] = None
        self._consumers: Dict[str, AIOKafkaConsumer] = {}
        self._consumer_tasks: Dict[str, asyncio.Task] = {}

    async def initialize(self) -> None:
        """Initialize Kafka producer."""
        logger.info("Initializing Kafka message queue...")

        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.settings.kafka_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            compression_type="gzip",
        )

        await self._producer.start()
        logger.info("Kafka producer initialized successfully")

    async def close(self) -> None:
        """Close all Kafka connections."""
        logger.info("Closing Kafka connections...")

        # Stop all consumers
        for topic, task in list(self._consumer_tasks.items()):
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

        for consumer in self._consumers.values():
            await consumer.stop()

        # Stop producer
        if self._producer:
            await self._producer.stop()

        logger.info("Kafka connections closed")

    async def produce(
        self,
        topic: str,
        message: Any,
        key: Optional[str] = None,
    ) -> bool:
        """Produce a message to a Kafka topic.

        Args:
            topic: Topic name
            message: Message to send (will be JSON serialized)
            key: Optional message key for partitioning

        Returns:
            True if successful, False otherwise

        Example:
            await mq.produce("core.identity.requests", {
                "action": "create",
                "data": {...}
            })
        """
        if not self._producer:
            raise RuntimeError("Message queue not initialized. Call initialize() first.")

        try:
            key_bytes = key.encode("utf-8") if key else None

            await self._producer.send_and_wait(
                topic,
                value=message,
                key=key_bytes,
            )

            logger.debug(f"Produced message to topic '{topic}'")
            return True

        except KafkaError as e:
            logger.error(f"Failed to produce message to topic '{topic}': {e}")
            return False

    async def consume(
        self,
        topic: str,
        handler: Callable[[Dict[str, Any]], Any],
        group_id: Optional[str] = None,
    ) -> None:
        """Start consuming messages from a Kafka topic.

        Args:
            topic: Topic name to consume from
            handler: Async function to handle each message
            group_id: Consumer group ID (default from settings)

        Example:
            async def handle_message(message):
                print(f"Received: {message}")

            await mq.consume("core.identity.requests", handle_message)
        """
        if topic in self._consumers:
            logger.warning(f"Already consuming from topic '{topic}'")
            return

        group_id = group_id or self.settings.kafka_consumer_group

        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.settings.kafka_servers,
            group_id=group_id,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
            auto_offset_reset="earliest",
        )

        await consumer.start()
        self._consumers[topic] = consumer

        # Start consumer task
        task = asyncio.create_task(self._consume_loop(topic, consumer, handler))
        self._consumer_tasks[topic] = task

        logger.info(f"Started consuming from topic '{topic}' in group '{group_id}'")

    async def _consume_loop(
        self,
        topic: str,
        consumer: AIOKafkaConsumer,
        handler: Callable[[Dict[str, Any]], Any],
    ) -> None:
        """Internal loop to consume messages.

        Args:
            topic: Topic name
            consumer: Kafka consumer instance
            handler: Message handler function
        """
        try:
            async for message in consumer:
                try:
                    # Call handler with message value
                    if asyncio.iscoroutinefunction(handler):
                        await handler(message.value)
                    else:
                        handler(message.value)

                except Exception as e:
                    logger.error(
                        f"Error handling message from topic '{topic}': {e}",
                        exc_info=True,
                    )

        except asyncio.CancelledError:
            logger.info(f"Consumer for topic '{topic}' cancelled")
        except Exception as e:
            logger.error(f"Error in consume loop for topic '{topic}': {e}")

    async def stop_consuming(self, topic: str) -> None:
        """Stop consuming from a topic.

        Args:
            topic: Topic name to stop consuming from
        """
        if topic not in self._consumers:
            logger.warning(f"Not consuming from topic '{topic}'")
            return

        # Cancel consumer task
        if topic in self._consumer_tasks:
            self._consumer_tasks[topic].cancel()
            try:
                await self._consumer_tasks[topic]
            except asyncio.CancelledError:
                pass
            del self._consumer_tasks[topic]

        # Stop consumer
        consumer = self._consumers[topic]
        await consumer.stop()
        del self._consumers[topic]

        logger.info(f"Stopped consuming from topic '{topic}'")

    async def create_topic(
        self,
        topic: str,
        num_partitions: int = 3,
        replication_factor: int = 1,
    ) -> bool:
        """Create a Kafka topic.

        Note: This requires admin permissions and may not work in all environments.

        Args:
            topic: Topic name
            num_partitions: Number of partitions
            replication_factor: Replication factor

        Returns:
            True if successful, False otherwise
        """
        try:
            from kafka.admin import KafkaAdminClient, NewTopic

            admin_client = KafkaAdminClient(
                bootstrap_servers=self.settings.kafka_servers,
            )

            topic_list = [
                NewTopic(
                    name=topic,
                    num_partitions=num_partitions,
                    replication_factor=replication_factor,
                )
            ]

            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            admin_client.close()

            logger.info(f"Created topic '{topic}'")
            return True

        except Exception as e:
            logger.error(f"Failed to create topic '{topic}': {e}")
            return False

    async def health_check(self) -> bool:
        """Check Kafka connection health.

        Returns:
            True if Kafka is healthy, False otherwise
        """
        try:
            if not self._producer:
                return False

            # Try to get cluster metadata
            metadata = await self._producer.client.fetch_all_metadata()
            return len(metadata.brokers) > 0

        except Exception as e:
            logger.error(f"Kafka health check failed: {e}")
            return False

    @property
    def producer(self) -> AIOKafkaProducer:
        """Get the Kafka producer."""
        if not self._producer:
            raise RuntimeError("Message queue not initialized. Call initialize() first.")
        return self._producer


# Global message queue manager instance
_mq_manager: Optional[MessageQueueManager] = None


async def get_message_queue() -> MessageQueueManager:
    """Get the global message queue manager instance.

    Returns:
        MessageQueueManager: Global message queue manager

    Example:
        mq = await get_message_queue()
        await mq.produce("topic", {"data": "value"})
    """
    global _mq_manager

    if _mq_manager is None:
        _mq_manager = MessageQueueManager()
        await _mq_manager.initialize()

    return _mq_manager


async def close_message_queue() -> None:
    """Close the global message queue manager."""
    global _mq_manager

    if _mq_manager:
        await _mq_manager.close()
        _mq_manager = None
