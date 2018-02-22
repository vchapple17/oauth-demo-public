# oauth-demo-public

## Who

Author: Val Chapple

## What

Demonstartion of the OAuth 2.0 handshake using Python 2.7 and Google App Engine.

## When

Jan 2018

## Where

Demo page can be found here: https://stately-century-142323.appspot.com/

## Why

Develop understanding of the handshake process of OAuth 2.0 without the abstraction of a third party library.

## How

An in-depth tutorial is located on Medium https://medium.com/@valeriechapple/how-to-truly-understand-oauth-2-0-69dd3e7574c6

However, here are the basic steps for those more familiar with Registering for APIs.

* Register an app on through Google's Cloud console, saving the client ID and secret.
* Through Google register your redirects, possibly localhost or the hosting url.
* Download repo.
* Update the config.py file with your client ID and secret.
* Update the const.py file with your webapp's base URL.
* Deploy app either locally or through Google App Engine.





