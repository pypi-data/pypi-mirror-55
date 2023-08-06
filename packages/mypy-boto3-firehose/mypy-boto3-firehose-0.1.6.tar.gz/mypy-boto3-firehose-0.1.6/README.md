# Mypy-boto3 firehose submodule

Provides type annotations for boto3 firehose service

## Installation

```bash
pip install mypy-boto3[firehose]
```

## Usage

```python
import boto3
from mypy_boto3.firehose import Client, ServiceResource

client: Client = boto3.client("firehose")
resource: ServiceResource = boto3.resource("firehose")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

