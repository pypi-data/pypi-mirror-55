# StreamLabs Python Library

This is the official python client for the StreamLabs Developer API.

## Documentation

See the [StreamLabs Developer API docs](https://developer.streamlabswater.com/docs/index.html)


Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package

```shell

pip3 install streamlabswater-streamlabswater

```

## Usage

The package needs to configured with your accounts API Key available when you  login into your [http://my.streamlabswater.com](http://my.streamlabswater.com) account.

```python

from streamlabswater import Stream

stream = Stream('YOUR_STREAMLABSWATER_API_KEY')

```

### Get all Locations
Start by fetching all your [locations](https://developer.streamlabswater.com/docs/get-all-locations.html)

```python

locations = stream.get_locations()

```

### Get a Location
A `location_id` is required to fetch details of a [location](https://developer.streamlabswater.com/docs/get-a-location.html), water usage and for updating *homeAway*.

```python

location_id = locations[0]['location_id']

my_home = stream.get_location(location_id)

```

### Update a Location
Currently you can only update the *homeAway* mode of the location
When updating a location the response is always the [updated location](https://developer.streamlabswater.com/docs/update-a-location.html) details

```python

# Set to home
my_home = stream.update_location(location_id, 'home')

# Set to away
my_home = stream.update_location(location_id, 'away')

```

### Subscribe to Location Alerts
If you choose to recieve notifications when alerts become active or end for a location, you need to provide a valid url endpoint where the StreamLabs service will send the notifications. The following methods wrap the corresponding StreamLabs api endpoints as descriped in the [Subscribe to Location Alerts section in the docs](https://developer.streamlabswater.com/docs/subscribe-to-location-alerts.html)

#### Create Subscription
```python

subscription_id = stream.subscribe_to_location_alerts(location_id, 'https://your-endpoint')['subscription_id']

```
#### Confirm subscription
Once you recieve the `confirmationToken` via your endpoint, update the subscription to start recieving alerts.

```python
confirmation_token = 'CONFIRMATION_TOKEN'

subscription = stream.confirm_subscription(subscription_id, confirmation_token)

# subscription['status'] should be 'confirmed'

```

### Get all Location Subscriptions

```python

subscriptions = stream.get_location_subscriptions(location_id)

```

### Get a Subscription

```python

subscription = stream.get_subscription(subscription_id)

```

### Get all Subscriptions

```python

all_subscriptions = stream.get_subscriptions()

```

### Delete a Subscription

```python

stream.delete_subscription(subscription_id)

```
This method will throw an Exception if the delete fails else returns a `None`

### Get a Location’s Water Usage Summary


```python

water_usage_summary = stream.get_location_water_usage_summary(location_id)

today = water_usage_summary['today']
this_month = water_usage_summary['thisMonth']
this_year = water_usage_summary['thisYear']
units = water_usage_summary['units']

```

### Get a Location’s Water Usage

At the very minimum you need to provide a `startTime` for the reading you want to retrive.

```python
from datetime import datetime, timezone, timedelta

yesterday = datetime.now(timezone.utc) - timedelta(days=1)
start_time = yesterday.isoformat(timespec='seconds')

usage = stream.get_location_water_usage(location_id, {'startTime': start_time})
```

## Credits

This project was heavily inspired by [streamlabswater-python](https://github.com/cpopp/streamlabswater-python)