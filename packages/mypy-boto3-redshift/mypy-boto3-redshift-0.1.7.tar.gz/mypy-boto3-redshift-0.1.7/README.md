# mypy-boto3-redshift submodule

Provides type annotations for `boto3.redshift` service

## Installation

```bash
pip install mypy-boto3[redshift]
```

## Usage

```python
import boto3
from mypy_boto3.redshift import Client, ServiceResource

client: Client = boto3.client("redshift")
resource: ServiceResource = boto3.resource("redshift")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

