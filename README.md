# food-bridge
## To connect to RDS database
make sure you have foodbridge.pem downloaded
for each file, run this command: scp -i ~/.ssh/foodbridge.pem /path/file_name.py ec2-user@54.245.187.177:~/ (do this each time you edit a file)
then run: ssh -i ~/.ssh/foodbridge.pem ec2-user@54.245.187.177
in the ec2 terminal, run your code