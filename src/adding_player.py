from pprint import pprint
import boto3
def put_player(name, password,dynamodb=None): 
    if not dynamodb:
        db = boto3.resource('dynamodb', region_name='us-east-1')
    table = db.Table('Players')
    response = table.put_item(
       Item={
            'name': name,
            'info':{
        'password': password}
        })

    return response
if __name__ == '__main__':
    movie_resp1 = put_player("Shaheer", "1234")
    movie_resp2 = put_player("Noor", "21342")
    movie_resp3 = put_player("Jim", "m213jn")
    print("Put Player succeeded:")
    pprint(movie_resp1, sort_dicts=False)