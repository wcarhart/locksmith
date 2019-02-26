# locksmith
*Your liaison between repository secrets and the great beyond.*

## Overview
`locksmith` acts as an interface between secrets and the Python code using them.

### Use case
Consider the following scenario: *Your cool new app requires a slick, unique API key to run. Perhaps your framework requires you to put this API key in a `manifest.json` or `AppDelegate` file. However, your manifest file(s) need to be checked into GitHub, thus exposing your precious API key. `locksmith` provides a layer of security to prevent you from having to type out your secrets in plaintext anywhere in your repository.*

### How it works
`locksmith` uses [`GnuPG`](https://www.gnupg.org/) to encrypt your secrets. Each user in your repository can have their own secrets, either shared among many or unique to each user. Then, `locksmith` exposes a simple API to access your secrets in code, rather than typing out something like `API_KEY = "something_that_shouldn't_be_shared"`.

## Installation
Install with `pip`:
```
pip3 install locksmith
```

Also, make sure you have `gpg` installed. You can use [`Homebrew`](https://brew.sh/):
```
brew install gpg
```

## Setup and Background
First, decide on who's going to be using your secrets. `locksmith` looks for secrets based on users, which are programmer-defined. For example, if I was the only user of my repo, the only user would be `wcarhart`. However, perhaps you're collaborating on a repo, where you'd have two users, such as `wcarhart` and `friend_user`. Or, perhaps you're collaborating on a repo but you'd only like to use one joint user for `locksmith`, such as `locksmith_user`.

If you have one user, `locksmith_user`, add the following file `locksmith_user.lcksmth` to your repository (but do NOT check it into version control!):
```
secret0=secret_value0
secret1=secret_value1
...
secretN=secret_valueN
```
An example of this file with actual values could be:
```
API_KEY=3eWhJtewSr0sSshNX9STOLUV1nGtFznxQM8UfyYH
DATABASE_USER=admin
DATABASE_AUTH=password
```
If you named this file `locksmith_user.lcksmth`, then these secrets will be available to the user `locksmith_user`, or to any user that knows `locksmith_user`'s password.

Now, encrypt the file using `gpg`:
```
gpg -c locksmith_user.lcksmth
```
This will produce a file `locksmith_user.lcksmth.gpg`. You can now safely check this into your version control

## Usage and API
### Usage
First, make sure to include `locksmith` in your Python code:
```
from locksmith import Locksmith
```
Then, make a `Locksmith` object based on what user(s) you have defined:
```
l = Locksmith("locksmith_user")
```
When the above line is executed, you will be prompted for `locksmith_user`'s password. This will happen only when you instatiate a new `Locksmith` object and not every time you access a secret.

### API
*`locksmith` exposes the following API for you to use*
#### `get_secret(parameter)`
The `get_secret` function allows you to get a specific secret, specified by `parameter`. Use it like this:
```
secret_value = l.get_secret("API_KEY")
```
If you pass in an invalid `parameter`, `locksmith` will raise a `ValueError` `LookupError`.

#### `add_secret(secret, value)`
The `add_secret` function allows you to add a secret on the fly to your secrets. Use it like this:
```
l.add_secret("API_KEY", "some_secret_value")
```
Note that this exposes your `some_secret_value` in plaintext. It's better practice to put your secret in the `locksmith_user.lcksmth` file before encrypting it. If you pass in an invalid `secret` or `value`, `locksmith` will raise a `ValueError` or `LookupError`.

#### `update_secret(secret, value)`
The `update_secret` function allows you to update one of your secrets on the fly. Use it like this:
```
l.update_secret("API_KEY", "some_secret_value")
```
Note that this exposes your `some_secret_value` in plaintext. It's better practice to put your secret in the `locksmith_user.lcksmth` file before encrypting it. If you pass in an invalid `secret` or `value`, `locksmith` will raise a `ValueError` or `LookupError`.

#### `save()`
If you make a change using `add_secret` or `update_secret`, you'll have to call the `save` function to persist your changes. Use it like this:
```
l.add_secret("API_KEY", "1234")
l.update_secret("API_KEY", "5678")
l.save()
```
Note that this exposes your `some_secret_value` in plaintext. It's better practice to put your secret in the `locksmith_user.lcksmth` file before encrypting it. This function is a WIP.
