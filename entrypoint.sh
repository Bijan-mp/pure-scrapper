echo "Waiting for mongo-db..."

while ! nc -z $MONGO_HOST $MONGO_PORT ; do
  sleep 0.1
done

echo "Mongo-db started"
echo "Waiting for server to RUN"
cd /home/src
python3 -m unittest test
python3 main.py