# mypy-boto3-lakeformation submodule

Provides type annotations for `boto3.lakeformation` service

## Installation

```bash
pip install mypy-boto3[lakeformation]
```

## Usage

```python
import boto3
from mypy_boto3.lakeformation import Client, ServiceResource

client: Client = boto3.client("lakeformation")
resource: ServiceResource = boto3.resource("lakeformation")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

