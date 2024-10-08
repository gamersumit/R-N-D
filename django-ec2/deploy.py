# How to deploy a/multiple django project on a single ec2 instance
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

4. Create Virtual Enviorement: 
    -- python3 -m venv projectnameenv       # you use should choose the name which resembels your project to avoid confusion for yourself.
    
    -- multiple project:  You should create sperperate/multiple environments for different projects to deploy multiple projects on same ec2 instance.

5. Clone the repositroy:
    -- git clone https://github.com/erkamesen/django_project.git
    -- checkout the branch which you want to deploy

    -- multiple project: Repeat this for multiple projects to deploy.

6. Install requirements for all the projects
    -- this will be the path ===> pwd : /home/ubuntu/django_project1
    -- this will be the path ===> pwd : /home/ubuntu/django_project2
    -- this will be the path ===> pwd : /home/ubuntu/django_project3

    
    -- source project1env/bin/activate
    -- pip3 install -r django_project1/requirements.txt
    -- deactivate

    -- mulitple project: 
        - carefully chose the enviroment to activate for the respective project to install the its requirement.txt of the project than deactive and do this with all the projects needed to be deployed.
        
7. Edit settings.py of the all the projects
    -- sudo nano django_project/settings.py
    -- We add our public IP and Domain name(Optional) to the ALLOWED_HOSTS list.
    -- Change DEBUG to False
    -- You can press CTRL-X and then Y to exit nano editor with save it.

8. Nginx Config
    -- sudo apt-get install -y nginx
    -- After nginx is installed, you can go to the public IP address from your browser and test it.
    -- Create django.conf for nginx
    -- sudo nano /etc/nginx/sites-avilable/django.conf
    -- Fill out the template below with your own values and save it

    -- NOTE: MULTIPLE PROJECTS: location /url/:  should be the different for each project it can be anything but must be different.
                -- it will distinguish requests for multiple projects. Like a request beongs to which project ?
                -- for example let's consider we have three django projects to deploy on the single ec2 instance, named as project1 and project2 and project3.
                -- this ts the public ip or base endpoint of our ec2 : xx-yy-xx-yy,    base endpoint = http://xx-yy-xx-yy/
                -- than all the project1 url should start with a specific word to bind its request to the project one for example url1.
                -- a request for the project1 should look like this: http://xx-yy-xx-yy/url1/register or http://xx-yy-xx-yy/url1/login or http://xx-yy-xx-yy/url1/dashboard.
                -- a request for the project3 should have url like: http://xx-yy-xx-yy/url3/credit 
                -- you have to configure these same urls in the projects too. so if your project url is base/register for than it should be base/url1/register now.
                -- you can choose any word or url to distingiush but it should be different for all the projects.
        ***
            server {

                listen 80;

                server_name <domain or public ip> ;

                location /url1/ {
                    include proxy_params;
                    proxy_pass http://unix:/home/ubuntu/<project1>/app.sock;
                }
                location /url2/ {
                    include proxy_params;
                    proxy_pass http://unix:/home/ubuntu/<project2>/app.sock;
                }
                location /url3/ {
                    include proxy_params;
                    proxy_pass http://unix:/home/ubuntu/<project3>/app.sock;
                }
                

                # STATIC FILES 
                location /url1/static/ {
                        alias /home/ubuntu/<project_folder_name>/static;
                }
                location /url2/static/ {
                        alias /home/ubuntu/<project_folder_name>/static;
                }
                location /url3/static/ {
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
    -- create gunicorn config: sudo nano /etc/supervisor/conf.d/project1.conf
    -- create gunicorn config: sudo nano /etc/supervisor/conf.d/project2.conf
    -- create gunicorn config: sudo nano /etc/supervisor/conf.d/project3.conf
    -- USE THE TEMPLATE for all the gunicorns
    ***
        [program:gunicorn]
        directory=/home/ubuntu/project1
        command=/home/ubuntu/projectenv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/project1/app.sock project1appname.wsgi:application  
        autostart=true
        autorestart=true

        stderr_logfile=/var/log/gunicorn/project1.err.log
        stdout_logfile=/var/log/gunicorn/project1.out.log

        user=www-data
        group=www-data
    ***

    -- create the above file for all the projects
    -- Create log directory: sudo mkdir /var/log/gunicorn/
    -- Run server:
    -- sudo supervisorctl reread
    -- sudo supervisorctl update
    -- sudo supervisorctl restart project1
    -- sudo supervisorctl restart project2
    -- sudo supervisorctl restart project3
    -- sudo supervisorctl status 
    -- Check app.sock: cd /home/ubuntu/django_project/
    -- ls
    -- if app.sock file exsist in every project than everything's working well
    -- restart nginx : sudo systemctl restart nginx
10. Create .env and other necessary file to the same directories and make sure all paths are correct you can start testing your apis.     

'''