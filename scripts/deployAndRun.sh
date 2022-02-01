#run with 'rshell -f deploy.sh'
#make sure RSHELL_PORT env variable is set (printenv RSHELL_PORT) to /dev/ttyUSB0
rsync ./src /pyboard/
repl ~ import clock ~ clock.run() ~ print("deploy script has run") ~