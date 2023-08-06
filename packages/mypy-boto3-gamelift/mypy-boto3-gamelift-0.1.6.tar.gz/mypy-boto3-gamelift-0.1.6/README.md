# Mypy-boto3 gamelift submodule

Provides type annotations for boto3 gamelift service

## Installation

```bash
pip install mypy-boto3[gamelift]
```

## Usage

```python
import boto3
from mypy_boto3.gamelift import Client, ServiceResource

client: Client = boto3.client("gamelift")
resource: ServiceResource = boto3.resource("gamelift")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

