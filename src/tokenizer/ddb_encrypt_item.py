import boto3
import os

from dynamodb_encryption_sdk.encrypted.table import EncryptedTable
from dynamodb_encryption_sdk.identifiers import CryptoAction
from dynamodb_encryption_sdk.material_providers.aws_kms import AwsKmsCryptographicMaterialsProvider
from dynamodb_encryption_sdk.structures import AttributeActions

aws_cmk_id=os.environ['KMSKey']

def encrypt_item (plaintext_item,table_name):
    table = boto3.resource('dynamodb').Table(table_name)

    aws_kms_cmp = AwsKmsCryptographicMaterialsProvider(key_id=aws_cmk_id)

    actions = AttributeActions(
        default_action=CryptoAction.ENCRYPT_AND_SIGN,
        attribute_actions={'Account_Id': CryptoAction.DO_NOTHING}
    )

    encrypted_table = EncryptedTable(
        table=table,
        materials_provider=aws_kms_cmp,
        attribute_actions=actions
    )
    
    #print (plaintext_item)
    response = encrypted_table.put_item(Item=plaintext_item)

    print(response)
    return response 

def get_decrypted_item (index_key,table_name):
    table = boto3.resource('dynamodb').Table(table_name)

    aws_kms_cmp = AwsKmsCryptographicMaterialsProvider(key_id=aws_cmk_id)

    actions = AttributeActions(
        default_action=CryptoAction.ENCRYPT_AND_SIGN,
        attribute_actions={'Account_Id': CryptoAction.DO_NOTHING}
    )

    encrypted_table = EncryptedTable(
        table=table,
        materials_provider=aws_kms_cmp,
        attribute_actions=actions
    )


    response = encrypted_table.get_item(Key=index_key)
    
    return response


def get_item (index_key,table_name):
    #table_name='CreditCardTokenizerTable'
    table = boto3.resource('dynamodb').Table(table_name)

    response = table.get_item(Key=index_key)

    return response 
