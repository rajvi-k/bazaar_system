#!/bin/sh

# install the libraries
pip3 install Flask --user
pip3 install pandas --user






# ssh into elnux3 and run the front end server

ssh elnux3.cs.umass.edu <<'END_SSH'
lsof -t -i tcp:35303 | xargs kill -9

set -x  # verbose output
cd ~/lab-3-lab-3-gupta-kapadia/src/front_end
# Start a process in the background and redirect its outputs. Nohup
# makes sure it won't die when SSH terminates.
nohup python3 frontend_server1.py --c '3'> front_end_output.txt 2>&1 &
echo $! > front_end.pid  # Save process id for later
echo "Front End PID: $(cat front_end.pid)"
END_SSH

# start catalog server on elnux 2
ssh elnux2.cs.umass.edu <<'END_SSH'
lsof -t -i tcp:50001 | xargs kill -9
lsof -t -i tcp:50002 | xargs kill -9

lsof -t -i tcp:35306 | xargs kill -9
lsof -t -i tcp:35307 | xargs kill -9


set -x  # verbose output
cd ~/lab-3-lab-3-gupta-kapadia/src/catalog
# Start a process in the background and redirect its outputs. Nohup
# makes sure it won't die when SSH terminates.
nohup python3 catalog_server2.py --c '3' --i '1'> catalog_server_output1.txt 2>&1 &
echo $! > catalog_server.pid  # Save process id for later
echo "catalog_server PID: $(cat catalog_server.pid)"
nohup python3 catalog_server2.py --c '3' --i '2'> catalog_server_output2.txt 2>&1 &
echo $! > catalog_server2.pid  # Save process id for later
echo "catalog_server PID: $(cat catalog_server2.pid)"
END_SSH


# start order server on elnux 1
ssh elnux1.cs.umass.edu <<'END_SSH'
set -x  # verbose output


lsof -t -i tcp:35300 | xargs kill -9
lsof -t -i tcp:35310 | xargs kill -9

cd ~/lab-3-lab-3-gupta-kapadia/src/order
lsof -t -i tcp:50003 | xargs kill -9
lsof -t -i tcp:35301 | xargs kill -9

nohup python3 order_server2.py --c '3' --i '1'> order_server1_output.txt 2>&1 &
echo $! > order_server.pid  # Save process id for later
echo "Order server PID: $(cat order_server.pid)"
nohup python3 order_server2.py --c '3' --i '2'> order_server2_output.txt 2>&1 &
echo $! > order_server2.pid  # Save process id for later
echo "Order server PID: $(cat order_server2.pid)"
END_SSH



# kill the catalog server 2 and restart it
ssh elnux2.cs.umass.edu <<'END_SSH'



cd ~/lab-3-lab-3-gupta-kapadia/src/catalog
echo "=======================Running tests =========================="
python3 ../tests/client.py --c '3'
lsof -t -i tcp:50002 | xargs kill -9
lsof -t -i tcp:35307 | xargs kill -9
nohup python3 resync.py --c '3' --i '2'> resync.output.txt 2>&1 &
nohup python3 restart_catalog.py --c '3' --i '2' > restart_catalog_output.txt 2>&1 &

END_SSH
sleep 5

echo "=========================Running tests after restarting and resyncing the catalog server ============================"
cd ~/lab-3-lab-3-gupta-kapadia/src
python3 tests/client.py --c '3'
