# Mypy-boto3 sms-voice submodule

Provides type annotations for boto3 sms-voice service

## Installation

```bash
pip install mypy-boto3[sms-voice]
```

## Usage

```python
import boto3
from mypy_boto3.sms_voice import Client, ServiceResource

client: Client = boto3.client("sms-voice")
resource: ServiceResource = boto3.resource("sms-voice")

# now your IDE can suggest you method and arguments names
# and mypy can check types
```

