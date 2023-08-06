# mypy-boto3-emr submodule

Provides type annotations for `boto3.emr` service

## Installation

```bash
pip install mypy-boto3[emr]
```

## Usage

```python
import boto3
from mypy_boto3.emr import Client, ServiceResource

client: Client = boto3.client("emr")
resource: ServiceResource = boto3.resource("emr")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

