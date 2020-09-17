# plugin-googleoauth2

Plugin for Google OAuth2

# Configuration

~~~python
options(dict) = {
	'client_id': '<client_id_text>',
	'domain': '<domain name>',
	'auth_type': 'google_oauth2'
}
~~~

# Example

~~~python
options(dict) = {
	'client_id': 'dflksdjfsdlkfjsd',
	'domain': 'gmail.com',
	'auth_type': 'google_oauth2'
}
~~~

# Release Note

## Version 1.1

Support New Auth API
* Auth.init
* Auth.verify

Identity Service >= 1.3.2
