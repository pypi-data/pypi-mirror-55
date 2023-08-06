# Mypy-boto3 codecommit submodule

Provides type annotations for boto3 codecommit service

## Installation

```bash
pip install mypy-boto3[codecommit]
```

## Usage

```python
import boto3
from mypy_boto3.codecommit import Client, ServiceResource

client: Client = boto3.client("codecommit")
resource: ServiceResource = boto3.resource("codecommit")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

