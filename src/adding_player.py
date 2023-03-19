from pprint import pprint
import boto3
from botocore.exceptions import ClientError



def get_player(name, password,dynamodb=None): 
    if not dynamodb:
        db = boto3.resource('dynamodb', region_name='us-east-1')
    table = db.Table('Players')
    #check if key is in table

    try:
        response = table.get_item(
       Key={
            'name': name,
        })
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        resp_pass = response['Item']['info']['password']
        if resp_pass == password:
            return "Success"
        else:
            return "Wrong password"
        # return response['Item']['info']['password']




def put_player(name, password,dynamodb=None): 
    if not dynamodb:
        db = boto3.resource('dynamodb', region_name='us-east-1')
    table = db.Table('Players')
    try:
        response = table.put_item(
        Item={
                'name': name,
                'info':{
            'password': password}
            },       ConditionExpression="attribute_not_exists(#name)",
            ExpressionAttributeNames={
                '#name': 'name'
            })
        print("Put Player succeeded:")
        print(response['Item'])
        return "Success"
    except:
        print("Player already exists")
        return get_player(name, password)


if __name__ == '__main__':
    movie_resp1 = put_player("Shaheer", "1234")
    # movie_resp2 = put_player("Noor", "21342")
    # movie_resp3 = put_player("Jim", "m213jn")
    # print("Put Player succeeded:")
    # pprint(movie_resp1, sort_dicts=False)
    #aa = get_player("Shaheer", "1234")
    # print("Get Player succeeded:")
    pprint(movie_resp1, sort_dicts=False)