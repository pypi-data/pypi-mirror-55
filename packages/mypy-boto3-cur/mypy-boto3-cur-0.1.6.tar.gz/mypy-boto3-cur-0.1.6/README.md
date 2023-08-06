# Mypy-boto3 cur submodule

Provides type annotations for boto3 cur service

## Installation

```bash
pip install mypy-boto3[cur]
```

## Usage

```python
import boto3
from mypy_boto3.cur import Client, ServiceResource

client: Client = boto3.client("cur")
resource: ServiceResource = boto3.resource("cur")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

