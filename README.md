Twitter-Hatena
================

post tweet of a day to hatenablog.com

System Requirements
-----------------
* Twitter account must be public
    * Twitter-Hatena gets timeline w/o authentication
* [Pit](http://d.hatena.ne.jp/jYoshiori/20080623/1214219490)
    * Pit for python is already registerd to Pypi
    * `sudo easy_install pit`
* Python 3 is not supported
    * todo

Usage
-----------------
    $ twitter_hatena.py [-d] [date(YYYY-MM-DD)]

* -d: Debug. Print to stdout instead of post to Hatena.
* date: Specify day to be post. Default is yesterday.

Credential
-----------------
Twitter-Hatena requires credentials of Twitter and Hatena.
Credentials are managed by Pit.

* hatena_domain: Domain of Hatenablog(e.g. wataken44.hatenablog.com)
* hatena_password: Password of Hatena
* hatena_username: Username of Hatena
* twitter_screenname: Username of Twitter(e.g. wataken44)


Limitation
-----------------
* Twitter account must be public
* Twitter-hatena