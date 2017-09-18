# actualizer

## cli

### list

*Options*
- `--start` :: `datetime`
- `--end` :: `datetime`
- `--username` :: `str`

By default, lists all log entries in the past week

### get-nutrition-info

*Options*
- `--day` :: `date`

Returns ordered dict mapping `datetime` of entry to `calories` and `food`

### log

*Options*

- `--message` :: `str` : The message to log.

e.g `"ate 500 cals of pie 2 hours ago"`

