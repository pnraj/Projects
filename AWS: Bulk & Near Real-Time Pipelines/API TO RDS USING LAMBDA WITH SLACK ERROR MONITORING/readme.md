<h1 align="center">API TO RDS USING LAMBDA WITH SLACK ERROR MONITORING </h1>

<p align="center">
  <img src="https://github.com/pnraj/Projects/assets/29162796/fe89c91f-a1ab-46e9-b589-4e9ef1bafa5a" alt="Project WorkFlow" width="990" height="590">
</p>

### Problem Statement:
- Configure _**AWS LAMBDA**_ to Fetch _**API**_ and Insert into _**AWS RDS**_  For Every _**15 Seconds**_ Interval with _Error Monitoring_ in _**Slack**_.

  ```json
  {"iss_position": {"longitude": "-173.8032", "latitude": "8.9644"}, "message": "success", "timestamp": 1688462894}

  ```


 ### Requirements:
 - Python <= 3.10
 - mysql-connector-python==8.0.26
 - slack_sdk
 - AWS Account with _**Admin Access**_


 ### Steps:

 - Create **`AWS RDS` Mysql Instance** and Create **Database and Table** for _API_ Insertion.
 ```sql
      CREATE DATABASE apidb;

      USE apidb;

      CREATE TABLE apitable (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Longitude DECIMAL(10, 4),
        Latitude DECIMAL(10, 4),
        Timestamp DATETIME
      );
  ```
 
 ```py
      def mysqlconn(host, port, user, password, longa, lat, unix_timestamp):
        try:
            conn = mysql.connect(host=host,port=port,
                user=user, password=password,
                database="apidb", raise_on_warnings=True,
                autocommit=True, connect_timeout=6  # Set the connection timeout to 6 seconds
            )
            
            if conn.is_connected():
                cur = conn.cursor()
                qur = "INSERT INTO apitable (Longitude, Latitude, Timestamp) VALUES (%s, %s, FROM_UNIXTIME(%s))"
                cur.execute(qur, (longa, lat, unix_timestamp))
                cur.close()
                conn.close()
            else:
                raise Exception("Failed to connect to the database")
        except mysql.Error as e:
            raise Exception(f"Database error- {e}")
```
 
 - Create **Api_Query Lambda** Function with Features to Fetch _API_ using Python inbuilt _**urllib.request**_ Module and Insert into Mysql Database Table using Python _**Mysql.connector**_.
      ```py
          def apitodb(host, port, user, password):
              url = "http://api.open-notify.org/iss-now.json"
              
              try:
                  response = urllib.request.urlopen(url)
                  dic = json.loads(response.read().decode())
                  longa, lat = dic["iss_position"]["longitude"], dic["iss_position"]["latitude"]
                  unix_timestamp = dic["timestamp"]
                  message = dic['message']
                  if message == "success":
                      mysqlconn(host, port, user, password, longa, lat, unix_timestamp)
                      return {"Message":"Successfully Inserted"}
              except Exception as e:
                  error_message = {"LambdaToRDS": f"{str(e)}"}
                  return error_message
      ```
    
    - **`AWS Lambda`** does not have Libraries needed for this Project so we have to Zip the needed libraries locally and upload the zip into _First Lambda_ Environment.
      ```py
        pip install mysql-connector-python==8.0.26 --target .
      ```
    
    - If any error Happens While _**Fetching API**_ or _**Connecting With Database**_ or _**Inserting Data into Database**_, A _**Slack**_ Notification Was Raised through __`Slack Api`__ from First Lambda.
      ```py
          def LambdaToSlack(token,ch_id,slack):
            client = WebClient(token=token)
            try:
              # Call the chat.postMessage method to send the message
              response = client.chat_postMessage(channel=ch_id, text=str(slack))
            except SlackApiError as e:
              return f"Error sending message: {e.response['error']}"

 - Create _**Iterator Lambda**_ Function with Features to _Triggering/Invoking_ **`Api_Query Lambda`** Function.
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

 - Create _**AWS Step Function**_ for triggering _**`Iterator Lambda`**_ at interval of _**15 seconds**_ using _ASL(Amazon States Language)_

  ```json
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


 

