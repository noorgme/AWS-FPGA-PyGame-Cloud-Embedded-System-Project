import boto3

def create_players(dynamodb=None):
    if not dynamodb:
        db = boto3.resource('dynamodb', region_name='us-east-1')
    table = db.create_table(
        TableName='Players',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1000,
            'WriteCapacityUnits': 1000
        }
    )
    return table

if __name__ == '__main__':
    player_table = create_players()
    print("Table status:", player_table.table_status)
