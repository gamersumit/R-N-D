# How to deploy a django project on ec2 instance
'''
1. Open Terminal : On your pc where we downloaded the key pair file open terminal.
    -- run the following command 
    -- chmod 700 /path/to/your-keypair.pem   
    -- ssh -i /path/to/your-keypair.pem username@public-ip-or-dns
    -- clear
    -- ls

2. Install and update
    -- sudo apt-get update
    -- sudo apt-get upgrade

3. Install virtual enviorement
    -- sudo apt-get install python3-venv
    -- cd /home/ubuntu/

4. Create Virtual Enviorement
    -- python3 -m venv 
    -- source venv/bin/activate

5. Clone the repositroy
    -- git clone https://github.com/erkamesen/django_project.git
    -- checkout the branch which you want to deploy
    -- cd to repository
    -- this will be the path ===> pwd : /home/ubuntu/django_project

6. Install requirements
    -- pip3 install -r requirements.txt

7. Edit settings.py
    -- sudo nano django_project/settings.py
    -- We add our public IP and Domain name(Optional) to the ALLOWED_HOSTS list.
    -- Change DEBUG to False
    -- You can press CTRL-X and then Y to exit nano editor with save it.

8. Nginx Config
    --  sudo apt-get install -y nginx
    --  After nginx is installed, you can go to the public IP address from your browser and test it.
    -- Create django.conf for nginx
    -- sudo nano /etc/nginx/sites-avilable/django.conf
    -- Fill out the template below with your own values and save it
        ***
            server {

                listen 80;

                server_name <domain or public ip> ;

                location / {
                    include proxy_params;
                    proxy_pass http://unix:/home/ubuntu/<project_folder_name>/app.sock;
                }

                # STATIC FILES 
                location /static/ {
                        alias /home/ubuntu/<project_folder_name>/static;
                }

            }
        
        ***

    -- Link to /sites-enabled
    -- sudo ln /etc/nginx/sites-available/django.conf /etc/nginx/sites-enabled/
    -- Check nginx status
    -- sudo nginx -t 
    -- if test result in success you have done well upto this point.
    -- Restart server
    -- sudo service nginx restart

9. Gunicorn & Supervisor
    -- Install Gunicorn: pip3 install gunicorn
    -- Install Supervisor: sudo apt-get install supervisor
    -- create gunicorn config: sudo nano /etc/supervisor/conf.d/gunicorn.conf
    -- USE THE TEMPLATE
    ***
        [program:gunicorn]
        directory=/home/ubuntu/<appname>
        command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/<appname>/app.sock <appname>.wsgi:application  
        autostart=true
        autorestart=true

        stderr_logfile=/var/log/gunicorn/gunicorn.err.log
        stdout_logfile=/var/log/gunicorn/gunicorn.out.log

        user=www-data
        group=www-data
    ***
    -- Create log directory: sudo mkdir /var/log/gunicorn/
    -- Run server:
    -- sudo supervisorctl reread
    -- sudo supervisorctl update
    -- sudo supervisorctl restart gunicorn
    -- sudo supervisorctl status
    -- Check app.sock: cd /home/ubuntu/django_project/
    -- ls
    -- if app.sock file exsist here than everything's working well
    -- restart nginx : sudo service nginx restart

10. Create .env and other necessary file to the same directories and make sure all paths are correct you can start testing your apis.     

'''