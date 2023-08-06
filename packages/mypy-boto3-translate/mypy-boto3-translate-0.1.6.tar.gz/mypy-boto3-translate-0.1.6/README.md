# Mypy-boto3 translate submodule

Provides type annotations for boto3 translate service

## Installation

```bash
pip install mypy-boto3[translate]
```

## Usage

```python
import boto3
from mypy_boto3.translate import Client, ServiceResource

client: Client = boto3.client("translate")
resource: ServiceResource = boto3.resource("translate")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

