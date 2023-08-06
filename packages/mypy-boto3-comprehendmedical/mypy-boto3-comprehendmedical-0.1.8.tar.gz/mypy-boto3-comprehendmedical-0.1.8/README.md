# mypy-boto3-comprehendmedical submodule

Provides type annotations for `boto3.comprehendmedical` service

## Installation

```bash
pip install mypy-boto3[comprehendmedical]
```

## Usage

```python
import boto3
from mypy_boto3.comprehendmedical import Client, ServiceResource

client: Client = boto3.client("comprehendmedical")
resource: ServiceResource = boto3.resource("comprehendmedical")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

