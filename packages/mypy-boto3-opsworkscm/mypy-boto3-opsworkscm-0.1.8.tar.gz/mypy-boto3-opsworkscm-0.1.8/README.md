# mypy-boto3-opsworkscm submodule

Provides type annotations for `boto3.opsworkscm` service

## Installation

```bash
pip install mypy-boto3[opsworkscm]
```

## Usage

```python
import boto3
from mypy_boto3.opsworkscm import Client, ServiceResource

client: Client = boto3.client("opsworkscm")
resource: ServiceResource = boto3.resource("opsworkscm")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

