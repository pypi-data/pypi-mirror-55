# Mypy-boto3 lightsail submodule

Provides type annotations for boto3 lightsail service

## Installation

```bash
pip install mypy-boto3[lightsail]
```

## Usage

```python
import boto3
from mypy_boto3.lightsail import Client, ServiceResource

client: Client = boto3.client("lightsail")
resource: ServiceResource = boto3.resource("lightsail")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

