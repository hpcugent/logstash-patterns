# Logstash patterns

Patterns for parsing and structuring log messages for different
services with [Logstash](http://logstash.net).

Use [this app](https://grokdebug.herokuapp.com/) for debugging your
patterns! Be careful, there might be subtle differences!

When issuing pull requests to this repository, don't forget to include an example of the messages your commits try to parse!!


# Adding pattern

Develop a new pattern typically in its own file, and call the main new pattern `<something>_MSG`.

Than you can do:
 * extend the `RSYSLOGMESSAGE` in the `rsyslog` file with a new pattern,
   by joining it with a `|` and placing the new pattern before the `GREEDYDATA` one.
   This requires only a new rpm and no configuration changes. This is very convient for
   testing.
 * add the new pattern to the list in the test configuration to the `grok`
   filter before the `RSYSLOGMESSAGE` as follows: `%{RSYSLOGPREFIX}%{<something>_MSG}`
   This requires a new rpm and configuration change in quattor too. Should only be done
   when a pattern is considered stable.

