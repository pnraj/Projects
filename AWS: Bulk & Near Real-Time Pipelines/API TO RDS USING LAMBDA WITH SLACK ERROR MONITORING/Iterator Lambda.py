import boto3

client = boto3.client('lambda')

def lambda_handler(event, context):
    index = event['iterator']['index'] + 1
    response = client.invoke(
        FunctionName='LAMBDA_TO_INVOKE',
        InvocationType='Event'
    )
    return {
            'index': index,
            'continue': index < event['iterator']['count'],
            'count': event['iterator']['count']
        }