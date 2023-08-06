<p align="center"><img src="https://pushradar.s3-eu-west-2.amazonaws.com/v2/img/pushradar_github.png"></p>

## Introduction

[PushRadar](https://www.pushradar.com) is a realtime notifications API service for the web. The service uses a simple publish-subscribe model, allowing you to broadcast "notifications" on "channels" that are subscribed to by one or more clients. Notifications are pushed in realtime to those clients.

PushRadar features advanced targeting options, including the ability to target clients by actions they have taken on your website or web app, geographical location (countries & continents), IP address, web browser and user ID.

This is PushRadar's official Python library.

## Prerequisites

In order to use this library, please ensure that you have the following:

- Python 3.3.0 or later.
- A PushRadar account - you can sign up at [www.pushradar.com](https://www.pushradar.com).

## Installation

The easiest way to get up and running is to install the library using [Pip](https://packaging.python.org/tutorials/installing-packages/). Run the following command in your console:

```
pip install PushRadar
```

## Getting Started

"Hello World!" example:

```python
from PushRadar import PushRadar

radar = PushRadar("your-secret-key")
radar.broadcast("test-channel", message="Hello World!")
```

## Receiving Notifications

To subscribe to channels and receive notifications broadcast on them, check out the documentation for PushRadar's [JavaScript client library](https://www.pushradar.com/documentation/latest/javascript).

## Fluent Syntax

The library supports fluent method chaining to structure broadcasts. For example, to target a notification to website visitors in the US who have not used live chat before:

```python
radar.target_country("US").target_not_action("live-chat").broadcast("test-channel",
    message="Would you like to talk to one of our customer support team members on live chat?")
```

Please note that targeting options reset after each call to the `broadcast` method.

## Private and Presence Channels

Private and presence channels require authentication before subscribers can receive messages on them.

To generate a channel authentication token, PushRadar provides a convenient `channel_auth` method that you can call from your authentication endpoint:

```python
return json.dumps({"authToken": radar.channel_auth("channel-name")})
```

Please note that private channels must start with the prefix 'private-' and presence channels must start with the prefix 'presence-'.

## Documentation

Full documentation for PushRadar's Python library can be found at: [www.pushradar.com/documentation/latest/python](https://www.pushradar.com/documentation/latest/python).