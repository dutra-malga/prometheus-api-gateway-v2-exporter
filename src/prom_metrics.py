import boto3

from dataclasses import dataclass
from prometheus_client import Gauge
from concurrent.futures import ThreadPoolExecutor

@dataclass
class PromMetrics():
    count = Gauge('count', 'Request count', ['route'])
    latency = Gauge('Latency', 'Api gateway latency', ['route'])
    integration_latency = Gauge('IntegrationLatency', 'Api gateway integration latency', ['route'])
    count_5xx = Gauge('count_5xx', 'Api gateway 5xx errors', ['route'])
    count_4xx = Gauge('count_4xx', 'Api gateway 4xx errors', ['route'])
    error_percent = Gauge('error_percent', 'Api gateway error percent', ['route'])

    def prometheus_metrics(self, apigw, max_workers):
        routes = apigw.list_routes()
        process = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for route in routes:
                process.append(executor.submit(
                    self.count.labels(route=route.get('RouteKey')).set(
                        apigw.get_route_statistics(
                            route.get('Method'), 
                            route.get('RouteKey'),
                            'Sum',
                            'Count'
                        )
                    )
                ))

                process.append(executor.submit(
                    self.latency.labels(route=route.get('RouteKey')).set(
                        apigw.get_route_statistics(
                            route.get('Method'), 
                            route.get('RouteKey'),
                            'Average',
                            'Latency'
                        )
                    )
                ))

                process.append(executor.submit(
                    self.integration_latency.labels(route=route.get('RouteKey')).set(
                        apigw.get_route_statistics(
                            route.get('Method'), 
                            route.get('RouteKey'),
                            'Average',
                            'IntegrationLatency'
                        )
                    )
                ))

                process.append(executor.submit(
                    self.count_5xx.labels(route=route.get('RouteKey')).set(
                        apigw.get_route_statistics(
                            route.get('Method'), 
                            route.get('RouteKey'),
                            'Sum',
                            '5xx'
                        )
                    )
                ))
    
                process.append(executor.submit(
                    self.count_4xx.labels(route=route.get('RouteKey')).set(
                        apigw.get_route_statistics(
                            route.get('Method'), 
                            route.get('RouteKey'),
                            'Sum',
                            '4xx'
                        )
                    )
                ))

                process.append(executor.submit(
                    self.error_percent.labels(route=route.get('RouteKey')).set(
                        apigw.error_percent(route.get('Method'), route.get('RouteKey'))
                    )
                ))
