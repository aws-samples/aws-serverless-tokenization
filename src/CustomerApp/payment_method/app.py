import json
import hash_gen
import ddb_encrypt_item
import boto3
import os
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    
    if (event['httpMethod'] == 'POST' and event['resource'] == '/order'):
        table_name = os.environ['EncryptionTableName']
        body = json.loads(event['body'])
        credit_card_token = hash_gen.get_uuid()
        print ("printing token value:", credit_card_token)
        ACCOUNT_ID = context.invoked_function_arn.split(":")[4]
        tokenize_request = {}
        tokenize_request['Hash_Key'] = str(credit_card_token)
        tokenize_request['Account_Id'] = ACCOUNT_ID
        tokenize_request['CandidateString'] = body.get('CreditCard')
        response = ddb_encrypt_item.encrypt_item(tokenize_request,table_name)
        
        ## Storing Items in DynamoDB 
        client = boto3.resource('dynamodb')
        cutomer_table = os.environ['CustomerOrderTableName']
        ddbtable = client.Table(cutomer_table)
        
        response = ddbtable.put_item(
                   Item={
                    'CustomerOrder': body.get('CustomerOrder'),
                    'CustomerName': body.get('CustomerName'),
                    'CreditCardToken' : str(credit_card_token),
                    'Address' : body.get('Address')
                        })
        print (response)
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Order Created Successfully",
                "CreditCardToken" : tokenize_request['Hash_Key']
            }),
        }
        
    if (event['httpMethod'] == 'POST' and event['resource'] == '/paybill'):
            table_name = os.environ['EncryptionTableName']
            body = json.loads(event['body'])
            #credit_card_token = hash_gen.get_uuid()
            #print ("printing token value:", credit_card_token)
            ACCOUNT_ID = context.invoked_function_arn.split(":")[4]
            ## Fetch Hash Key from Customer Order Table
            client = boto3.resource('dynamodb')
            cutomer_table = os.environ['CustomerOrderTableName']
            ddbtable = client.Table(cutomer_table)
            try:
                responseddb = ddbtable.get_item(
                                    Key={
                                            'CustomerOrder' : body.get('CustomerOrder')
                                        })
            except ClientError as e:
                print(e.response['Error']['Message'])
                return {
                    "statusCode": 500,
                     "body": json.dumps({
                    "message": "Payment Submission Failed"
                    }),
                    }
            else:
                item = responseddb['Item']
                print(item)
                index_key = {}
                index_key['Hash_Key'] = item['CreditCardToken']
                index_key['Account_Id'] = ACCOUNT_ID
                response2 = ddb_encrypt_item.get_decrypted_item(index_key,table_name)
                ### Add your code to invoke bill payment API
                ##print(response2)
                return {
                    "statusCode": 200,
                     "body": json.dumps({
                    "message": "Payment Submitted Successfully",
                    "CreditCard Charged" : response2['Item']['CandidateString']
                    }),
                    }
        
    if (event['httpMethod'] == 'GET' and event['resource'] == '/hello'):
            return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Hello from Lambda!"
            }),
        }



