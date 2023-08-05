# -*- coding: utf-8 -*-
import psycopg2, re, os
import urllib.parse as urlparse

class Database:
    """A database connection/interface; use this to connect to your postgresql
    database and interact with it. This is a psycopg2 wrapper used at
    www.imerir.com to ease database operations by students when lecturing
    Web Services."""
    
    def __init__(self, connOption=None):
        """Creates an instance of `Db`. One why provide a posgresql URL as
        parameter, or provide None to use the `DATABASE_URL` def environment
        variable. (This particularly integrates well with Heroku)"""
        
        url = None
        urlparse.uses_netloc.append("postgres")
        if connOption is None:
            url = urlparse.urlparse(os.environ["DATABASE_URL"])
        elif type(connOption) is str:
            url = urlparse.urlparse(connOption)
        
        if url is not None:
            # Expected: postgres://[user[:password]@][netloc][:port][/dbname]
            self._conn = psycopg2.connect(
                database=url.path[1:],
                user=url.username,
                password=url.password,
                host=url.hostname,
                port=url.port
            )
        else:
            # Assume it is a connection object
            # Dangerous and untested: could be used to pass a MySQL Connector
            self._conn = connOption
        
        self._cur = self._conn.cursor()
        self._columns = None
    
    def _getColumnNames(self, subkeys = None):
        """Will return an array of column names. You may provide a `subkeys`
        dict to substitute some column names with other names."""
        
        columns = self._cur.description
        if columns is None:
            return None
        
        columnNames = [col[0] for col in columns]
        
        # substitute columns names for new ones
        if subkeys is not None:
            for (i, oldName) in enumerate(columnNames):
                if oldName in subkeys:
                    columnNames[i] = subkeys[oldName]
        
        return columnNames
    
    def _formatRows(self, row, columns):
        """Turns a result row into a dict with column names as keys."""
        return dict(zip(columns, row))

    def count(self):
        """Returns the number of rows."""
        count = self._cur.rowcount
        return count if count > -1 else None
    
    def columns(self):
        """Returns the columns."""
        if self._columns is not None:
            return self._columns[:]
        else:
            return [] # always return a list, prefer [] to None
    
    def execute(self, sql, sqlParams=None, subkeys=None):
        """Perform a SQL statements. This may be a SELECT, DELETE, CREATE, …"""
        
        if self._cur is None:
            raise ConnectionError('The connection was closed.')
        
        # reformat bindings from `:xyz` to `%(xyz)s` syntax.
        if sqlParams is not None:
            sql = re.sub(r":([a-zA-Z_]{1}[a-zA-Z0-9_]*)", "%(\g<1>)s", sql)
        
        # perform the actual query
        self._cur.execute(sql, sqlParams)
        
        # update the columns description
        if self._cur.rowcount != -1: # -1 for non-selecting statements
            self._columns = self._getColumnNames(subkeys)
        else:
            self._columns = None
        
        # commit (automatically commit for DELETE/INSERT/…)
        self._conn.commit()
    
    def fetchAll(self, subkeys = None):
        """Fetch all the returned rows for the last executed SQL statement."""
        rows  = self._cur.fetchall()
        if rows != None:
            rows = [self._formatRows(row, self._columns) for row in rows]
        else:
            rows = [] # always return a list, prefer [] to None
        return rows
    
    def fetchOne(self, subkeys = None):
        """Fetch returned rows by the last executed SQL statement one-by-one."""
        row  = self._cur.fetchone()
        if row != None:
            row = self._formatRows(row, self._columns)
        return row
    
    def executeAndFetchAll(self, sql, sqlParams=None, subkeys=None):
        """Performs an `execute` and then a `fetchAll`."""
        self.execute(sql, sqlParams)
        return self.fetchAll(subkeys)
    
    def executeFile(self, filename):
        """Loads file contents and executes them at once."""
        f = file(filename, "r")
        sql = f.read()
        f.close()
        self.execute(sql)
    
    def close(self):
        """Closes the connection and stops accepting commands."""
        self._cur.close()
        self._conn.close()
        
        self._cur = None
        self._conn = None
        self._columns = None
    
    def __enter__(self):
        return self
   
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
