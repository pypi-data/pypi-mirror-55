# Mypy-boto3 cloudsearchdomain submodule

Provides type annotations for boto3 cloudsearchdomain service

## Installation

```bash
pip install mypy-boto3[cloudsearchdomain]
```

## Usage

```python
import boto3
from mypy_boto3.cloudsearchdomain import Client, ServiceResource

client: Client = boto3.client("cloudsearchdomain")
resource: ServiceResource = boto3.resource("cloudsearchdomain")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

