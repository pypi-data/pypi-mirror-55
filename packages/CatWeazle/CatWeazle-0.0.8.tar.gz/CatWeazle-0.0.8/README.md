Introduction
************
CatWeazle is an application that will help you to register systems in dynamic environments, 
like AWS, to DNS (including A and PTR records) and RedHat IdM / FreeIPA.

DNS and IdM/IPA handling is mostly done using the "Smart Proxy" of the 
["The Foreman"](https://github.com/theforeman/smart-proxy) project. 
The Smart Proxy offers integration with most common DNS Servers, as well as RedHat IdM and FreeIPA.

AWS Route 53 integration is done directly in the API Server, using the AWS boto3 library. 
The reason for this is that the Smart Proxy Plugin for AWS will not support "Private hosted zones".

Here is an illustration on how the process works in AWS for EC2 instances:

```

```

It consists of the following parts:

API Server:

Provides an RESTful API that that will be used to register new systems. The API server 

Installing
----------

pip install catweazle

the configuration is expected to be placed in /etc/catweazle/config.ini

an example configuration looks like this

```
[main]
host = 0.0.0.0
port = 9000
domain_suffix = .us-east1.aws.example.com

[file:logging]
acc_log = catweazle_rest_access.log
acc_retention = 7
app_log = catweazle_rest.log
app_retention = 7
app_loglevel = DEBUG

[aws]
enable = true
arpa_zone_id = ZNTVAHUPY596W
zone_id = Z1YUAMV5C5Q71Z

[foreman]
url = https://fmsmart1-example.com:8443
ssl_crt = /etc/puppetlabs/puppet/ssl/certs/catweazle.example.com.pem
ssl_key = /etc/puppetlabs/puppet/ssl/private_keys/catweazle.example.com.pem
dns_enable = true
realm_enable = true
realm = EXAMPLE.COM

[session:redispool]
host = 192.168.33.12
#pass = dummy

[main:mongopool]
hosts = 192.168.33.12
db = catweazle
#pass =
#user =

[instances:mongocoll]
coll = instances
pool = main

[permissions:mongocoll]
coll = permissions
pool = main

[users:mongocoll]
coll = users
pool = main

[users_credentials:mongocoll]
coll = users_credentials
pool = main


```


Author
------

Stephan Schultchen <stephan.schultchen@gmail.com>

License
-------

Unless stated otherwise on-file foreman-dlm-updater uses the MIT license,
check LICENSE file.

Contributing
------------

If you'd like to contribute, fork the project, make a patch and send a pull
request.