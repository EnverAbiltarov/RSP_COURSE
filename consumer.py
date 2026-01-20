# consumer.py
import json
import logging
import time
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("kafka_consumer")

bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                "product-events",
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='product-group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            logger.info("Успешно подключено к Kafka!")
            return consumer
        except (KafkaError, Exception) as e:
            logger.warning("Не удалось подключиться к Kafka: %s | Повтор через 5 секунд...", e)
            time.sleep(5)

logger.info("Запуск консюмера, ожидание Kafka...")
consumer = create_consumer()

logger.info("Консюмер запущен, ждём события из темы product-events...")

try:
    for message in consumer:
        event = message.value
        try:
            event_type = event.get("type", "unknown")
            product = event.get("product", {})
            processed = f"Обработано: {event_type.upper()} товар '{product.get('name', 'неизвестно')}' (ID: {product.get('id', 'нет')})"
            logger.info(processed)
        except Exception as e:
            logger.error("Ошибка обработки сообщения: %s | Сообщение: %s", e, event)
except KeyboardInterrupt:
    logger.info("Остановка консюмера...")
    consumer.close()
except Exception as e:
    logger.error("Критическая ошибка консюмера: %s", e)
    raise