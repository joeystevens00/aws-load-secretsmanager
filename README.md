# AWS-Load-Secretsmanager
A utility that will print the key/values of secret from secretsmanager as export commands to make it easy to import them into the shell environment. When run from an ec2 instance it supports variables from tags in the form of python format variables

E.g. this will use the env tag from the current ec2 instance. If the tag env was set to stage then this will load the secrets from stage/service/config into the shell environment
```
`python3 load_secrets.py "{env}/service/config"`
```