# hns_notification
Thin wrapper around various notification systems. 

## Notifications available
1. Opsgenie

## Installation
`pip install hns-notification`

## Opsgenie usage
Below code snippet shows how to create alert on opsgenie. 
```python
# Your API key
api_key = 'api_key'

# Configure the opsgenie api. This would return you an api client object
api_client = configure(api_key)

# Create the alert, pass the api client and the alert message body. 
# Check https://docs.opsgenie.com/docs/python-sdk-alert#section-create-alert for details on accepted alert body fields.  
alert = create_alert(api_client, {
    'message': 'sample_msg',
    'alias': 'some-alias',
    'responders': [{
                'name': 'SampleTeam',
                'type': 'team'
              }],
    'visible_to': [
      {'name': 'Sample',
       'type': 'team'}],
    'actions': ['Restart', 'AnExampleAction'],
    'tags': ['OverwriteQuietHours'],
    'details': {'key1': 'value1',
             'key2': 'value2'},
    'entity': 'An example entity',
    'priority': 'P3',
    'description': 'Sample of SDK v2'
})

# This returns the opsgenie response object containing the request_id and result of create alert. 
print(alert)
```
