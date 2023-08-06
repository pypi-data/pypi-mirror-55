# Common Python Helper Functions

This project contains reusable code for various projects. Written in Python.

Documentation to be completed

## THINGS TO CONSIDER
- The logger library is expecting the following environment variables to send the log data to the logstash socket:
LOGSTASH_HOST
LOGSTASH_PORT
- If any of these variables is not present, the logging library will work as expected, without posting the logs to elasticsearch 