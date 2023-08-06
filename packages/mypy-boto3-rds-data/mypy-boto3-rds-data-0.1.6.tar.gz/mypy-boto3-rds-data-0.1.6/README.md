# Mypy-boto3 rds-data submodule

Provides type annotations for boto3 rds-data service

## Installation

```bash
pip install mypy-boto3[rds-data]
```

## Usage

```python
import boto3
from mypy_boto3.rds_data import Client, ServiceResource

client: Client = boto3.client("rds-data")
resource: ServiceResource = boto3.resource("rds-data")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

