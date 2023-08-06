# Mypy-boto3 iot1click-projects submodule

Provides type annotations for boto3 iot1click-projects service

## Installation

```bash
pip install mypy-boto3[iot1click-projects]
```

## Usage

```python
import boto3
from mypy_boto3.iot1click_projects import Client, ServiceResource

client: Client = boto3.client("iot1click-projects")
resource: ServiceResource = boto3.resource("iot1click-projects")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

