# how to create aws ec2 instance
'''
1. login into you aws account
2. go to ec2 dashboard
3. click on instances
4. click on launch instance
5. enter deatils 
    -- name : name of your instance
    -- application and operating system for your instance : ubuntu
    -- AMI (Amazon Machine Image) : Ubuntu server 24.04 LTS, Free tier eligible
    -- Instance type : t2.micro,  free tier eligible
    -- Create a key pair and download the .pem file
    -- Mark all three security rule :
         !! Allow SSH
         !! Allow HTTPS
         !! Allow HTTP
    -- Launch instance

6. wait until status check turns green    

7. Binding with the elastic IP
    -- in Newtork & Security Section of Ec2 dashboard click ELastic IPs
    -- click Allocate elastic ip address
    -- click allocate
    -- click on the ip
    -- click associate elastic ip address
    -- chose the instance to bind 
    -- fill the private ip of the instnace
    -- click on associate

-- Instance is created
'''
