import boto3
from configuration import aws_access_key_id, aws_secret_access_key

client = boto3.client("sns", aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,
                      region_name="eu-west-1")

test = "Treść sms2"

client.publish(PhoneNumber="+27648032037", Message=test)
