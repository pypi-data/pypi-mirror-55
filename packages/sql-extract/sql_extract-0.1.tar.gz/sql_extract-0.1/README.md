# sql_extract.py
Exports the results of Oracle sql code contained in a .sql file out to a csv file. 

## Usage
```bash
# make executable 
chmod +x sql_extract.py

# run 
./sql_extract.py in_sql_file.sql -o output_file.csv

# additional help
./sql_extract.py -h
```


## Parameters
| Name            | Description                         | Type   | Required |
|-----------------|-------------------------------------|--------|----------|
| filename        | input .sql file name                | string | yes      |
| -o, --outfile   | output .csv file name               | string | no       |
| -d, --delimiter | csv delimiter                       | string | no       |
| -c, --quotechar | csv quote character                 | string | no       |
| bind_vars       | any bind variables in the .sql file | list   | no       |

### Configuration
- "full_login" and "db_password" environment variables set accordingly

### Further Documentation
Additional documentation is available on the [SQL Extract confluence page](https://confluence.rowan.edu/display/ASA/SQL+Extract).