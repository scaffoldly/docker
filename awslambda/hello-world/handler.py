import json
import platform

def handler(event):
    print(f"Event: {event}")
    return "Hello world"

def apigateway(event, context):
    print(f"Context: {context}")
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(
            {
                "message": handler(event=event), 
                "runtime": platform.python_version()}
        ),
    }
