"""
Installation setup
"""

from setuptools import setup, find_packages

setup(
    name='prometheus-api-gateway-v2-exporter',
    version='0.0.1',
    description='Prometheus exporter for AWS API Gateway HTTP (v2)',
    url='https://github.com/bsdutra/prometheus-api-gateway-v2-exporter',
    author='Gabriel M. Dutra',
    author_email="bsdutra@proton.me",
    entry_points={"console_scripts": ["prometheus-api-gateway-v2-exporter=src.__main__:main"]},
    install_requires=[
        'boto3',
        'prometheus_client'
    ],
    zip_safe=False,
    packages=find_packages()
)
