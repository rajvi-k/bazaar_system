# 677 Lab 3

This is the Git repo for 677 Lab 3. See https://marcoserafini.github.io/teaching/distributed-os/spring20/labs/lab3.html for a description of the lab. The lab is due on Apr 24th, 11:59 pm. Prior to submitting your project, replace this README file with the one that explains how to setup and run your code. Be sure to provide enough details fo us to run it in order to grade it.


Instructions for running the code-
1. Ssh into elnux1 and login and clone repository in home diretory. Enter into lab-3-lab-3-gupta-kapadia
cd ~
git clone https://github.com/ds-umass/lab-3-lab-3-gupta-kapadia.git
cd lab-3-lab-3-gupta-kapadia
2. Change permissions of starter script: chmod +x src/starter.sh
3. Execute starter script:  ./src/starter.sh
4. Enter password when prompted
5. To view logs in the same folder there are files- front_end.log, order_server.log and catalog_server.log
6. To view the output of the servers it is saved in each of the folders inside src/

catalog/catalog_server_output1.txt

catalog/catalog_server_output2.txt

catalog/restart_catalog_output.txt

catalog/resync.output.txt

order/order_server1_output.txt

order/order_server2_output.txt

front_end/front_end_output.txt

This script installs the pre-requisites, starts servers, runs tests, kills catalog server, resyncs it and finally runs the tests again.

