# Mypy-boto3 elasticbeanstalk submodule

Provides type annotations for boto3 elasticbeanstalk service

## Installation

```bash
pip install mypy-boto3[elasticbeanstalk]
```

## Usage

```python
import boto3
from mypy_boto3.elasticbeanstalk import Client, ServiceResource

client: Client = boto3.client("elasticbeanstalk")
resource: ServiceResource = boto3.resource("elasticbeanstalk")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

