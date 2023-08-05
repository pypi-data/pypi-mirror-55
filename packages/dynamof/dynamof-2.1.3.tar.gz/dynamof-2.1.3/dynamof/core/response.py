
from boto3.dynamodb.types import TypeDeserializer

from dynamof.core.utils import strip_Decimals, immutable


def destructure_type_tree(data):

    if data is None:
        return None

    # Using `strip_Decimals` here to patch an
    # undesireable behavior with dynamo where
    # it takes in number types but always returns
    # Decimal class type.
    # https://github.com/boto/boto3/issues/369

    return strip_Decimals({
        k: TypeDeserializer().deserialize(v) for k, v in data.items()
    })

def response(res):

    return immutable({

        'retries': lambda: res.get('ResponseMetadata', {}).get('RetryAttempts', None),

        'success': lambda: res.get('ResponseMetadata', {}).get('HTTPStatusCode', 0) == 200,

        'item': lambda: destructure_type_tree(res.get('Item', None)),

        'items': lambda: [destructure_type_tree(item) for item in res.get('Items')] if res.get('Items', None) is not None else None,

        'count': lambda: res.get('Count', None),

        'scanned_count': lambda: res.get('ScannedCount', None),

        'raw': lambda: res

    })
