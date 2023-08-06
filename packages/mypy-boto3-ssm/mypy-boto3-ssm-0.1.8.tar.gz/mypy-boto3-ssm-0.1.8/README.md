# mypy-boto3-ssm submodule

Provides type annotations for `boto3.ssm` service

## Installation

```bash
pip install mypy-boto3[ssm]
```

## Usage

```python
import boto3
from mypy_boto3.ssm import Client, ServiceResource

client: Client = boto3.client("ssm")
resource: ServiceResource = boto3.resource("ssm")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

