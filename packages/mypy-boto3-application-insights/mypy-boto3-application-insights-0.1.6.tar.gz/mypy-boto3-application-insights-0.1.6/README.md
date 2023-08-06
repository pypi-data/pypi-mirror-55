# Mypy-boto3 application-insights submodule

Provides type annotations for boto3 application-insights service

## Installation

```bash
pip install mypy-boto3[application-insights]
```

## Usage

```python
import boto3
from mypy_boto3.application_insights import Client, ServiceResource

client: Client = boto3.client("application-insights")
resource: ServiceResource = boto3.resource("application-insights")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

