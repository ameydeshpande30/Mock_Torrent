source venv/bin/activate
cd full_nodes
cd node1
rm torrent.db
gnome-terminal -e "python3 app.py"
cd ..
cd node2
rm torrent.db
gnome-terminal -e "python3 app.py"
cd ..
cd node3
rm torrent.db
gnome-terminal -e "python3 app.py"
cd ..

curl localhost:5001/node -d '{"node": "http://127.0.0.1:5002"}' -H 'Content-Type: application/json'
curl localhost:5001/node -d '{"node": "http://127.0.0.1:5003"}' -H 'Content-Type: application/json'

curl localhost:5002/node -d '{"node": "http://127.0.0.1:5001"}' -H 'Content-Type: application/json'
curl localhost:5002/node -d '{"node": "http://127.0.0.1:5003"}' -H 'Content-Type: application/json'

curl localhost:5003/node -d '{"node": "http://127.0.0.1:5002"}' -H 'Content-Type: application/json'
curl localhost:5003/node -d '{"node": "http://127.0.0.1:5001"}' -H 'Content-Type: application/json'