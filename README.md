# Grok patterns

Patterns for parsing and structuring log messages for different
services with [Vector](http://vector.dev).

Use [this app](https://grokdebug.herokuapp.com/) for debugging your
patterns! Be careful, there might be subtle differences!

When issuing pull requests to this repository, don't forget to include an example of the messages your commits try to parse!!

## Adding pattern

Develop a new PATTERN typically in its own file, and call the main new pattern `<PATTERN>_MSG`.

Then you can:
  * Add the new message pattern to the Vector config file in the section `[transforms.syslog]`. Typically,
    you will add it to the top-level list of patterns to try (second argument of parse_groks).
  * Include the definitions for this grok pattern in its own JSON file `<PATTERN>.json`, in the format 
    given by the existing JSON files. You will need to add this filename to the `vector.toml` config file
    under the parse_groks argument `alias_sources`.
  * Add tests for your pattern in `tests/<PATTERN>.toml`. Specify the input, and compose the VRL program that 
    asserts the expected structured output.
