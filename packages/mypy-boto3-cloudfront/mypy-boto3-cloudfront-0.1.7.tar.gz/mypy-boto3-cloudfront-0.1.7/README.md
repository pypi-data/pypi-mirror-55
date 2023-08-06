# mypy-boto3-cloudfront submodule

Provides type annotations for `boto3.cloudfront` service

## Installation

```bash
pip install mypy-boto3[cloudfront]
```

## Usage

```python
import boto3
from mypy_boto3.cloudfront import Client, ServiceResource

client: Client = boto3.client("cloudfront")
resource: ServiceResource = boto3.resource("cloudfront")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

