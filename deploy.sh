# deploying to production

# On droplet ---------------------
# prune images and containers
# build new images
# Copy/create .env file on website/env_files folder.

# On website container -----------
# Run migrations from within website
python manage.py migrate
python manage.py migrate ali --database=ali
# If django superuser don't exist, create one.
# Generate translation files
python manage.py compilemessages
# Collect static files

# On website ---------------------
# Create periodic tasks
# Create tracker entry

# create cron job to run certbot every 15 days to update certificates