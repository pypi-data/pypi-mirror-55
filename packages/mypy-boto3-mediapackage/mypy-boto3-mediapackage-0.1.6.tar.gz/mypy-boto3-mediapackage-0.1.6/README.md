# Mypy-boto3 mediapackage submodule

Provides type annotations for boto3 mediapackage service

## Installation

```bash
pip install mypy-boto3[mediapackage]
```

## Usage

```python
import boto3
from mypy_boto3.mediapackage import Client, ServiceResource

client: Client = boto3.client("mediapackage")
resource: ServiceResource = boto3.resource("mediapackage")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

