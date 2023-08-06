# Mypy-boto3 dax submodule

Provides type annotations for boto3 dax service

## Installation

```bash
pip install mypy-boto3[dax]
```

## Usage

```python
import boto3
from mypy_boto3.dax import Client, ServiceResource

client: Client = boto3.client("dax")
resource: ServiceResource = boto3.resource("dax")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

