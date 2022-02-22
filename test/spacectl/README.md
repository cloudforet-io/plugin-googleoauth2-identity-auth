# Configuration

## Register Plugin

This is for registering plugin in local repository or portal.

Run as root domain

~~~
spacectl exec register repository.Plugin -c register_plugin.yaml
~~~


## Change Auth Plugin

* Update client_id
* Update domain

~~~
spacectl exec change_auth_plugin identity.Domain -c change_auth_plugin.yaml
~~~

