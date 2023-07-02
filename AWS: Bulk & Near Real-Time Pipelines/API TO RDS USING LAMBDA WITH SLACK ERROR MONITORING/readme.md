## API TO RDS USING LAMBDA WITH SLACK ERROR MONITORING

### Problem Statement:
Configure _**AWS LAMBDA**_ to Fetch _**API**_ and Insert into _**AWS RDS**_  For Every _**15 Seconds**_ Interval with _Error Monitoring_ in _**Slack**_.

<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/fe89c91f-a1ab-46e9-b589-4e9ef1bafa5a" alt="Project WorkFlow" width="990" height="650">
</p>




 ### Requirements:
 - Python <= 3.7
 - mysql-connector-python==8.0.26
 - slack_sdk
 - AWS Account with _**Admin Access**_


 ### Steps:

 - Create **`AWS RDS` Mysql Instance** and Create **Database and Table** in that instance for _API_ Insertion.
 - Create **First Lambda** Function with Features to Fetch _API_ using Python inbuilt _**urllib.request**_ Module and Insert into Mysql Database Table using Python _**Mysql.connector**_.

    - **`AWS Lambda`** does not have Libraries needed for this Project so we have to Zip the needed libraries locally and upload the zip into _First Lambda_ Environment.
      ```py
        pip install mysql-connector-python==8.0.26 --target .
      ```
    
    - If any error Happens While _**Fetching API**_ or _**Connecting With Database**_ or _**Inserting Data into Database**_, A _**Slack**_ Notification Was Raised through __`Slack Api`__ from First Lambda.

 - Create _**Second Lambda**_ Function with Features to _Triggering/Invoking_ **`First Lambda`** Function.
   ```py
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
   
   ```

 - Create _**AWS Step Function**_ for triggering _**`Second Lambda`**_ at interval of _**15 seconds**_ using _ASL(Amazon States Language)_

  ```py
        {
        "Comment": "Invoke Lambda every 15 seconds",
        "StartAt": "ConfigureCount",
        "States": {
            "ConfigureCount": {
                "Type": "Pass",
                "Result": {
                    "index": 0,
                    "count": 4
                },
                "ResultPath": "$.iterator",
                "Next": "Iterator"
            },
            "Iterator": {
                "Type": "Task",
                "Resource": "arn:aws:lambda:REGION:ACCOUNT_ID:function:Iterator",
                "ResultPath": "$.iterator",
                "Next": "IsCountReached"
            },
            "IsCountReached": {
                "Type": "Choice",
                "Choices": [
                    {
                        "Variable": "$.iterator.continue",
                        "BooleanEquals": true,
                        "Next": "Wait"
                    }
                ],
                "Default": "Done"
            },
            "Wait": {
                "Type": "Wait",
                "Seconds": 15,
                "Next": "Iterator"
            },
            "Done": {
                "Type": "Pass",
                "End": true
            }
        }
    }
  ```
  
 - Create _**AWS Cloud Watch(Rule)**_ to trigger Step Function for every _**One minute**_ interval between each triggering for Time Schedule that is required.


 

