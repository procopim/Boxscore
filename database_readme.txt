Do not install mysql. Find the version of mysql connector that matches your python version and OS from below. 

You must first initialize the data directory
https://dev.mysql.com/doc/refman/8.0/en/data-directory-initialization.html#data-directory-initialization-overview

(windows)
mysqld --initialize --console 

after initialization, open mysql CLI tool:
SET PASSWORD = 'some_pw';  (current on test machine is 'mark')


Then you start the mysql server before using the db module (windows):
https://dev.mysql.com/doc/refman/8.0/en/windows-start-command-line.html

start
cmd: mysqld --console
shutdown
cmd: mysqladmin shutdown

Please see link below for mysql instructions for Windows and Linux:
https://dev.mysql.com/downloads/connector/python/

Mysql documentation:
https://dev.mysql.com/doc/connector-python/en/connector-python-example-connecting.html

Some source inspiration:
https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html

Mysql CLI cheatsheet:
https://gist.github.com/hofmannsven/9164408 
