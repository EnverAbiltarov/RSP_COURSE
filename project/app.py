# app.py
import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import json
from kafka import KafkaProducer
import os

# ============================
# Логирование (как было)
# ============================
logger = logging.getLogger("shop_api")
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
file_handler = RotatingFileHandler("logs/app.log", maxBytes=5_000_000, backupCount=5, encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# ============================
# Kafka Producer
# ============================
bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    retries=5,
    acks='all'
)

TOPIC_NAME = "product-events"
DLQ_TOPIC = "product-events-dlq"  # Dead Letter Queue

def send_event(event_type: str, product: dict):
    event = {
        "type": event_type,
        "product": product,
        "timestamp": __import__('time').time()
    }
    try:
        producer.send(TOPIC_NAME, value=event)
        producer.flush()
        logger.info("Событие отправлено в Kafka | type=%s | id=%s", event_type, product.get("id"))
    except Exception as e:
        logger.error("Ошибка отправки в Kafka: %s | Отправляем в DLQ", e)
        try:
            producer.send(DLQ_TOPIC, value={**event, "error": str(e)})
            producer.flush()
        except:
            logger.critical("Не удалось отправить даже в DLQ")

# ============================
# FastAPI
# ============================
app = FastAPI(title="REST API с Kafka")

class Product(BaseModel):
    id: Optional[int] = None
    name: str
    price: float
    description: Optional[str] = None

products = [
    Product(id=1, name="Чайник", price=2500.0),
    Product(id=2, name="Тостер", price=3200.0)
]
next_id = 3

@app.get("/products", response_model=List[Product])
def list_products():
    logger.info("Запрос списка товаров | Всего: %d", len(products))
    return products

@app.get("/products/{product_id}", response_model=Product)
def get_product(product_id: int):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        logger.warning("Товар не найден | ID: %s", product_id)
        raise HTTPException(404, "Товар не найден")
    logger.info("Запрос товара | ID: %d | Название: %s", product_id, product.name)
    return product

@app.post("/products", response_model=Product, status_code=201)
def create(product: Product):
    global next_id
    product.id = next_id
    next_id += 1
    products.append(product)
    
    send_event("created", product.model_dump())
    logger.info("Создан товар | ID: %d | Название: %s", product.id, product.name)
    return product

@app.put("/products/{product_id}", response_model=Product)
def update(product_id: int, updated: Product):
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        logger.warning("Попытка обновить несуществующий товар | ID: %s", product_id)
        raise HTTPException(404, "Товар не найден")
    
    old_name = product.name
    updated.id = product_id
    products[products.index(product)] = updated
    
    send_event("updated", updated.model_dump())
    logger.info("Товар обновлён | ID: %d | Было: %s → Стало: %s", product_id, old_name, updated.name)
    return updated

@app.delete("/products/{product_id}")
def delete(product_id: int):
    global products
    product = next((p for p in products if p.id == product_id), None)
    if not product:
        logger.warning("Попытка удалить несуществующий товар | ID: %s", product_id)
        raise HTTPException(404, "Товар не найден")
    
    send_event("deleted", product.model_dump())
    products = [p for p in products if p.id != product_id]
    logger.info("Товар удалён | ID: %s | Название: %s", product_id, product.name)
    return {"message": "Удалено"}

if __name__ == "__main__":
    logger.info("Запуск сервера FastAPI...")
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True, log_level="info")