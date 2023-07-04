# final lambda function
import mysql.connector as mysql
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os, json,datetime, urllib.request

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

def LambdaToSlack(token,ch_id,slack):
  client = WebClient(token=token)
  try:
    # Call the chat.postMessage method to send the message
    response = client.chat_postMessage(channel=ch_id, text=str(slack))
  except SlackApiError as e:
    return f"Error sending message: {e.response['error']}"

def lambda_handler(event, context):
  host,user,port,password = os.getenv("host"), os.getenv("user"), int(os.getenv("port")), os.getenv("password")
  data = apitodb(host,port,user,password)
  
  if "LambdaToRDS" in data:
    ch_id, token = os.getenv("channel_id"), os.getenv("token")
    LambdaToSlack(token,ch_id,data)
    return data
  else:
    return data