# Django Cognito Authentication
The intent of this library is to provide a package that supports Django and allows an easy implementation for replacing the default Django authentication with an AWS Cognito based authentication.

This is a fork of [Alex Plants](https://github.com/Olorin92) great work with the original [django-cognito](https://github.com/Olorin92/django_cognito).

## Install

```
pip install django-cognito-redux
```

## AWS Credentials

This library uses boto3 which follows a specific path for determining what credentials to use. Definitely recommend reading their [Configuring Credentials](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html) section.

    The mechanism in which boto3 looks for credentials is to search through a list of possible locations and stop as soon as it finds credentials. The order in which Boto3 searches for credentials is:

    1. Passing credentials as parameters in the boto.client() method
    2. Passing credentials as parameters when creating a Session object
    3. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`, `AWS_PROFILE`)
    4. Shared credential file (~/.aws/credentials)
    5. AWS config file (~/.aws/config)
    6. Assume Role provider
    7. Boto2 config file (/etc/boto.cfg and ~/.boto)
    8. Instance metadata service on an Amazon EC2 instance that has an IAM role configured.

It is recommended to not pass in arguments with you instantiate a new session or client. Instead use IAM roles for production, and local configuration files locally.

As an example I generally have a profile setup in my `~/.aws/credentials`, and a default region set for that profile in `~/.aws/config`.
From there I set `AWS_PROFILE=profilename` as an environment variable so my app knows what to use. This allows for easy local development as well as
being able to use IAM roles in production, and not having to set a lot of environment variables.
