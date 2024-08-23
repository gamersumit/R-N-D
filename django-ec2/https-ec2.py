# HOW TO PROVIDE HTTPS SUPPORT TO YOUR EC2 INSTANCE
'''
1. FOLLOW THE 'http-ec2' file to deploy your django project on ec2 instance.

2. Buy a domain(sites google domain, godaddy etc.) for your site or skip if you already have one.

3. Point Domain to EC2 Instance
    --- Update the DNS settings of your domain to point to your EC2 instance's public IP address. 
    --- This typically involves creating an "A" record in your domain registrar's DNS settings.
        --- REGISTAR'S ACCOUNT : login into the site from where you purchased the domain.
        --- there will option in the settings to create a new record or to create A record.
        --- For the A Record:
            ***
                Type: A
                Host: @ (This represents the root domain, e.g., yourdomain.com)
                Value: Your EC2 instance’s public IP address. You can find this in your EC2 management console under the "Instances" section.
                TTL (Time to Live): You can usually leave this as the default value or set it to a lower value like 300 seconds (5 minutes) if you anticipate frequent changes
            ***
        
4. Install Certbot for SSL/TLS certificates
    --- Certbot is a tool that automates the process of obtaining and renewing Let's Encrypt SSL/TLS certificates.
    --- sudo apt-get install certbot python3-certbot-nginx
    --- sudo certbot --nginx

5. Configure Nginx for Your Django Project    
    --- /etc/nginx/sites-available/
    --- update django.conf : server_name yourdomain.com www.yourdomain.com;

    --- Test the nginx configuration :  sudo nginx -t
    --- Restart Nginx:  sudo systemctl restart nginx

6. Obtain an SSL Certificate Using Certbot
    -- Run Certbot to automatically obtain and configure the SSL certificate
    --- COMMAND TO RUN : sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
    -- Follow the prompts to complete the process. Certbot will automatically update your Nginx configuration to use HTTPS.

7. Auto-Renew the Certificate : VALIDITY OF SSL IS 90 days    
    -- Certbot takes care of renewing the certificates, but you can set up a cron job to ensure it runs regularly
    --- COMMAND :- sudo crontab -e
    -- Add the following line to the crontab to run Certbot twice daily:
    --- 0 0,12 * * * /usr/bin/certbot renew --quiet

8. Force Redirect HTTP to HTTPS (Optional)
    -- To automatically redirect HTTP traffic to HTTPS, update your Nginx configuration
    -- update  /etc/nginx/sites-available/django.config
    ***
        server {
            listen 80;
            server_name yourdomain.com www.yourdomain.com;
            return 301 https://$host$request_uri;
        }
    ***

    -- Restart Nginx : sudo systemctl restart nginx
'''

# Redirect HTTP to HTTPS
# final nginx django config file should look like this :-
'''
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com; # Replace with your domain

    location / {
        return 301 https://$host$request_uri;
    }
}

# HTTPS Server Block
server {
    listen 443 ssl;
    server_name yourdomain.com www.yourdomain.com; # Replace with your domain

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem; # Path to your certificate
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem; # Path to your private key

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/project/app.sock;

        proxy_connect_timeout 300s;
        proxy_read_timeout 300s;
        proxy_send_timeout 300s;
        send_timeout 300s;

        client_max_body_size 50M;
        client_body_buffer_size 128k;

        proxy_buffer_size 128k;
        proxy_buffers 4 256k;
        proxy_busy_buffers_size 256k;
    }

    # STATIC FILES 
    location /static/ {
        alias /home/ubuntu/AI_BOOK/static;
    }
}


'''