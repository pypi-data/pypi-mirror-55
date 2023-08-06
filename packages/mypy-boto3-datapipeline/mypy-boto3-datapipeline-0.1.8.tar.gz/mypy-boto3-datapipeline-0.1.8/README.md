# mypy-boto3-datapipeline submodule

Provides type annotations for `boto3.datapipeline` service

## Installation

```bash
pip install mypy-boto3[datapipeline]
```

## Usage

```python
import boto3
from mypy_boto3.datapipeline import Client, ServiceResource

client: Client = boto3.client("datapipeline")
resource: ServiceResource = boto3.resource("datapipeline")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

