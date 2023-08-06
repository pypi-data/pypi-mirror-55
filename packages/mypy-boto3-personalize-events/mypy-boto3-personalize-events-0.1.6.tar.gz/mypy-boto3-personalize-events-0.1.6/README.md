# Mypy-boto3 personalize-events submodule

Provides type annotations for boto3 personalize-events service

## Installation

```bash
pip install mypy-boto3[personalize-events]
```

## Usage

```python
import boto3
from mypy_boto3.personalize_events import Client, ServiceResource

client: Client = boto3.client("personalize-events")
resource: ServiceResource = boto3.resource("personalize-events")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

