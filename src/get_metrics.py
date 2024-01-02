import boto3
import datetime

class ApiGatewayMetrics():
    def __init__(self, api_id, stage, region="us-east-1"):
        self._api_id = api_id
        self._stage = stage
        self._region = region

    def _aws_client(self, resource):
        return boto3.client(resource, region_name=self._region)

    def get_route_statistics(self, method, resource, statistic, metric_name):
        client = self._aws_client('cloudwatch')

        end = datetime.datetime.utcnow()
        start = end - datetime.timedelta(minutes=1)

        dims = [
        {
            "Name": "ApiId",
            "Value": self._api_id
        },
        {
            "Name": "Method",
            "Value": method,
        },
        {
            "Name": "Resource",
            "Value": resource
        },
        {
            "Name": "Stage",
            "Value": self._stage
        }]

        res = client.get_metric_statistics(
            Namespace="AWS/ApiGateway",
            MetricName=metric_name,
            Dimensions=dims,
            StartTime=start,
            EndTime=end, 
            Period=60,
            Statistics=[statistic]
        )

        try:
            datapoints = res.get('Datapoints')
            datapoint = datapoints[-1].get(statistic)
        except IndexError:
            datapoint = 0

        return datapoint

    def error_percent(self, method, resource):
        count_5xx = self.get_route_statistics(method, resource, 'Sum', '5xx')
        count_4xx = self.get_route_statistics(method, resource, 'Sum', '4xx')
        count = self.get_route_statistics(method, resource, 'Sum', 'Count')

        try:
            percent = (count_5xx + count_4xx) * 100 / count
        except ZeroDivisionError:
            percent = 0
        
        return percent

    def list_routes(self):
        client = self._aws_client('apigatewayv2')
        items = client.get_routes(ApiId=self._api_id).get('Items')

        routes = []

        for item in items:
            routes.append({
                'Method': item.get('RouteKey').split()[0],
                'RouteKey': item.get('RouteKey').split()[1],
            })

        return routes
