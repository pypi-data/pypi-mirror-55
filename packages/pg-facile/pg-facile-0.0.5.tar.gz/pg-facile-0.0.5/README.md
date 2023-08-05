# pg-facile

An easy-to-use wrapper for psycopg2 for those who only care to type a SQL statement and get its result with column names in an easy to use format (namely: students).

## Disclaimer

This package is used within a Web Services course where students do not have much time to learn and practice the proper way of accessing databases in Python: https://www.python.org/dev/peps/pep-0249/

Indeed, databases are not the core of the course; the architecture is what matters most and students are quickly encouraged to use ORM libraries such as [SQLAlchemy](https://www.sqlalchemy.org) over typing their own SQL statements.

Please refrain from using this package. It is merely a small wrapper around `psycopg2` ([link](https://pypi.org/project/psycopg2/)).

## Getting Started

The following instructions illustrate how to use this package.

### Prerequisites

Ideally you should have installed the `virtualenv` command and Python 3.

Also, you will need access to a postgresql database. You should know how to describe the host and credentials in URL form; such as `postgres://[user[:password]@][netloc][:port][/dbname]`.

If you have Docker installed, then you may run `docker run -p 5432:5432 -e POSTGRES_PASSWORD=123456 --rm -d postgres` to start a local server whose URL will be: `postgres://postgres:123456@localhost:5432/postgres`.

### Installing

Using `pip`:

```
pip install pg-facile
```

Ideally this should be preceded by the creation and activation of a virtual environment:

```
virtualenv -p python3 venv
source venv/bin/activate
```

### Example

Here is an example using the `pg-facile` module:

```py
from pg-facile import Database

url = 'postgres://postgres:123456@localhost:5432/postgres'

with Database(url) as db:
  db.execute('CREATE TABLE numbers (value INTEGER)')
  
  for i in range(50):
    db.execute('INSERT INTO numbers(value) VALUES (:val)', {'val': i})


with Database(url) as db:
  rows = db.executeAndFetchAll('SELECT * FROM numbers WHERE value % 2 = 0')
  for row in rows:
    print(row)
```

## Contributing

No contributions are expected nor wanted. Yet, if you find a bug or which to enhance this humble package, you may:

  * contact the maintainer by email <[pierre.grabolosa@imerir.com](mailto:pierre.grabolosa@imerir.com)>
  * open an issue on the GitHub project repository,
  * submit a pull request.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/pgrabolosa/pg-facile/tags).

## Authors

See the list of [contributors](https://github.com/pgrabolosa/pg-facile/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
