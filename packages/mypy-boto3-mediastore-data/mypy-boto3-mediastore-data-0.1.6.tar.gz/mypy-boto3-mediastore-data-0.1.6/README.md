# Mypy-boto3 mediastore-data submodule

Provides type annotations for boto3 mediastore-data service

## Installation

```bash
pip install mypy-boto3[mediastore-data]
```

## Usage

```python
import boto3
from mypy_boto3.mediastore_data import Client, ServiceResource

client: Client = boto3.client("mediastore-data")
resource: ServiceResource = boto3.resource("mediastore-data")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

