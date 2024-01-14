"""
    Entrypoint to start prometheus HTTP server
"""

#!/usr/bin/env python

import sys
import time
import os

from prometheus_client import start_http_server
from src.get_metrics import ApiGatewayMetrics
from src.prom_metrics import PromMetrics

REFRESH_INTERVAL = int(os.environ.get("REFRESH_INTERVAL", 60))
PORT = int(os.environ.get("PORT", 8200))
REGION = os.environ.get("AWS_REGION", "us-east-1")
API_ID = os.environ.get("API_ID")
API_STAGE = os.environ.get("API_STAGE", "$default")
MAX_WORKERS = int(os.environ.get("MAX_WORKERS", 20))


def main():
    """
        ApiGatewayMetrics - Get AWS API Gateway metrics
        PromMetrics - Create metrics to prometheus
    """

    apigw = ApiGatewayMetrics(API_ID, API_STAGE)
    prom = PromMetrics()

    try:
        start_http_server(PORT)
    except OSError as error:
        print(error)
        sys.exit(1)

    while True:
        prom.prometheus_metrics(apigw, MAX_WORKERS)
        time.sleep(REFRESH_INTERVAL)

if __name__=='__main__':
    main()
