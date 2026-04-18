"""
pay-api: A simple Flask application for the SCA DevOps Bootcamp.

This app simulates a payment service with three endpoints:
  /          - Home page
  /payment   - Payment page
  /health    - Health check
  /metrics   - Prometheus metrics endpoint

It writes structured logs to stdout so Alloy/Promtail can collect them.
"""

import logging
import random
import time
from flask import Flask, request, jsonify, Response
from prometheus_client import (
    Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
)

# -- Logging Setup -----------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  level=%(levelname)s  logger=pay-api  msg=%(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)
logger = logging.getLogger("pay-api")

# -- Prometheus Metrics -------------------------------------------------------
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"],
)
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5],
)
PAYMENT_SUCCESS = Counter("payment_success_total", "Successful payments")
PAYMENT_FAILURE = Counter("payment_failure_total", "Failed payments")
APP_UP = Gauge("pay_api_up", "Whether pay-api is running")
APP_UP.set(1)

# -- Flask App ----------------------------------------------------------------
app = Flask(__name__)


@app.route("/")
def home():
    start = time.time()
    logger.info("endpoint=/ client=%s action=home_page_served", request.remote_addr)
    REQUEST_COUNT.labels(method="GET", endpoint="/", status="200").inc()
    REQUEST_LATENCY.labels(method="GET", endpoint="/").observe(time.time() - start)
    return "<h1>Welcome to Pay-API</h1><p>SCA DevOps Bootcamp - Monitoring Lab</p>"


@app.route("/payment")
def payment():
    start = time.time()
    delay = random.uniform(0.05, 0.5)
    time.sleep(delay)

    if random.random() < 0.05:
        PAYMENT_FAILURE.inc()
        REQUEST_COUNT.labels(method="GET", endpoint="/payment", status="500").inc()
        REQUEST_LATENCY.labels(method="GET", endpoint="/payment").observe(time.time() - start)
        logger.error(
            "endpoint=/payment client=%s action=payment_failed duration_ms=%.0f",
            request.remote_addr, delay * 1000,
        )
        return jsonify({"status": "error", "message": "Payment failed"}), 500

    PAYMENT_SUCCESS.inc()
    REQUEST_COUNT.labels(method="GET", endpoint="/payment", status="200").inc()
    REQUEST_LATENCY.labels(method="GET", endpoint="/payment").observe(time.time() - start)
    logger.info(
        "endpoint=/payment client=%s action=payment_success duration_ms=%.0f",
        request.remote_addr, delay * 1000,
    )
    return jsonify({"status": "success", "message": f"Payment processed in {delay*1000:.0f}ms"})


@app.route("/health")
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health", status="200").inc()
    return jsonify({"status": "healthy"})


@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    logger.info("action=startup msg=pay-api starting on port 5000")
    app.run(host="0.0.0.0", port=5000)
