import boto3
from .geohash import decode_exactly, decode, encode
from boto3.dynamodb.conditions import Key, And

# index.query(partition_key='value', lat=x, long=y, )

# https://www.movable-type.co.uk/scripts/geohash.html
# Length	Cell width	Cell height Size equivalent
# --------- ----------- ----------- ---------------
# 1         ≤ 5,000km	×	5,000km large country / continent
# 2         ≤ 1,250km	×	625km   region / state / small country
# 3         ≤ 156km	    ×	156km   metro area / county
# 4         ≤ 39.1km	×	19.5km  locality
# 5         ≤ 4.89km	×	4.89km  small locality
# 6         ≤ 1.22km	×	0.61km  neighborhood
# 7         ≤ 153m	    ×	153m    block
# 8         ≤ 38.2m	    ×	19.1m   house
# 9         ≤ 4.77m	    ×	4.77m   room
# 10        ≤ 1.19m	    ×	0.596m  person
# 11        ≤ 149mm	    ×	149mm   sheet of paper
# 12        ≤ 37.2mm	×	18.6mm  credit card

class SpatialIndex():

    def __init__(self, table, index_name):
        self.table = table
        self.index_name = index_name
        found = False
        for index_info in self.table.global_secondary_indexes:
            if index_info['IndexName'] == index_name:
                for k in index_info['KeySchema']:
                    if k['KeyType'] == 'HASH':
                        self.part_key = k['AttributeName']
                    elif k['KeyType'] == 'RANGE':
                        self.range_key = k['AttributeName']
                found = True
            break
        if not found:
            from botocore.exceptions import ValidationError
            raise ValidationError(param='IndexName', value=index_name, type_name='str')

    def query(self, part_value, lat, long, precision=7, **kwargs):
        hash = encode(lat, long, precision)
        res = self.table.query(
            IndexName=self.index_name,
            KeyConditionExpression=And(
                Key(self.part_key).eq(part_value),
                Key(self.range_key).begins_with(hash)),
            **kwargs
        )
        for item in res['Items']:
            lats, longs = decode(item[self.range_key])
            item['_lat'] = float(lats)
            item['_long'] = float(longs)
        return res
    
    def put_item(self, part_value=None, lat=None, long=None, item=None, batch_prep=False, **kwargs):
        if not item:
            item = {}
        if not part_value:
            part_value = item[self.part_key]
        if not lat:
            lat = item['lat']
        if not long:
            long = item['long']

        hash = encode(lat, long, precision=12)
        item[self.part_key] = part_value
        item[self.range_key] = hash
        if batch_prep:
            return item
        else:
            res = self.table.put_item(
                Item=item, **kwargs
            )
