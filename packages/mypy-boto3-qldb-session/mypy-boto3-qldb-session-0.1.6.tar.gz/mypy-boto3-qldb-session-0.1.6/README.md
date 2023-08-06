# Mypy-boto3 qldb-session submodule

Provides type annotations for boto3 qldb-session service

## Installation

```bash
pip install mypy-boto3[qldb-session]
```

## Usage

```python
import boto3
from mypy_boto3.qldb_session import Client, ServiceResource

client: Client = boto3.client("qldb-session")
resource: ServiceResource = boto3.resource("qldb-session")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

