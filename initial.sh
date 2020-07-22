#! /bin/bash
#sudo apt install python-dev
#sudo apt-get update
#sudo apt-get install -y build-essential
#sudo apt-get install -y python3.4-dev
#sudo apt-get install -y libpq-dev

#pip3 install psycopg2
function installPostgre()
{
	#rm -rf /var/lib/apt/lists/lock
	#sudo apt update 
	#sudo apt install postgresql postgresql-contrib
	
	
	
	
	#sudo -u postgres psql
	

	sudo -i -u postgres psql -c "CREATE DATABASE cognitus6 WITH ENCODING 'UTF-8' TEMPLATE=template0;" 
	sudo -i -u postgres psql -c "CREATE USER testuser WITH PASSWORD 'test';" 
	sudo -i -u postgres psql -c "ALTER ROLE testuser SET client_encoding TO 'utf8';" 
	sudo -i -u postgres psql -c "ALTER ROLE testuser SET default_transaction_isolation TO 'read committed';" 
	sudo -i -u postgres psql -c "ALTER ROLE testuser SET timezone TO 'UTC';" 
	sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE cognitus TO testuser;" 
	sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO testuser;"
	sudo -i -u postgres psql -c "ALTER USER testuser WITH SUPERUSER;"
	
}

function createTable()
{
	
	path="$(pwd)/test_data.csv"
	echo $path
	sudo -i -u postgres psql -d cognitus6 -c "CREATE TABLE dataset(id int PRIMARY KEY,text VARCHAR (255) ,label VARCHAR (255));"
	sudo -i -u postgres psql -d cognitus6 -c "COPY dataset(text,label) FROM '${path}' DELIMITER ',' CSV HEADER;"
	sudo -i -u postgres psql -d cognitus6 -c "SELECT * from dataset;"
	
}


if declare -f "$1" > /dev/null
then
  # call arguments verbatim
  "$@"
else
  # Show a helpful error
  echo "'$1' is not a known function name" >&2
  exit 1
fi

