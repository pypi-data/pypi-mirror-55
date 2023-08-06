# mypy-boto3-greengrass submodule

Provides type annotations for `boto3.greengrass` service

## Installation

```bash
pip install mypy-boto3[greengrass]
```

## Usage

```python
import boto3
from mypy_boto3.greengrass import Client, ServiceResource

client: Client = boto3.client("greengrass")
resource: ServiceResource = boto3.resource("greengrass")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

