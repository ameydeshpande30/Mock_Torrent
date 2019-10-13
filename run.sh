source venv/bin/activate
cd full_nodes
for i in 1 2 3
do 
	rm -rf node$i
	cp -R node node$i
	cd node$i
	rm torrent.db
	gnome-terminal -e "python3 app.py 500$i"
	cd ..
done

sleep 5s
curl localhost:5001/node -d '{"node": "127.0.0.1:5002"}' -H 'Content-Type: application/json'
curl localhost:5001/node -d '{"node": "127.0.0.1:5003"}' -H 'Content-Type: application/json'

curl localhost:5002/node -d '{"node": "127.0.0.1:5001"}' -H 'Content-Type: application/json'
curl localhost:5002/node -d '{"node": "127.0.0.1:5003"}' -H 'Content-Type: application/json'

curl localhost:5003/node -d '{"node": "127.0.0.1:5002"}' -H 'Content-Type: application/json'
curl localhost:5003/node -d '{"node": "127.0.0.1:5001"}' -H 'Content-Type: application/json'
cd ..
cd Peers
for i in 1 2 3
do
	rm -rf Peer$i
	cp -R Peerfinal Peer$i
done
cd ..
