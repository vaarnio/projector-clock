#run with 'rshell -f deploy.sh'
#make sure RSHELL_PORT env variable is set (printenv RSHELL_PORT)
rsync . /pyboard/
repl ~ import lcd ~ lcd.run() ~ print("deploy script has run") ~