# mypy-boto3-macie submodule

Provides type annotations for `boto3.macie` service

## Installation

```bash
pip install mypy-boto3[macie]
```

## Usage

```python
import boto3
from mypy_boto3.macie import Client, ServiceResource

client: Client = boto3.client("macie")
resource: ServiceResource = boto3.resource("macie")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

