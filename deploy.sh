# deploying to production

# On droplet ---------------------
# Copy/create .env file on website/env_files folder.

# On website container -----------
# If django superuser don't exist, create one.
# Run migrations from within website
python manage.py migrate
python manage.py migrate ali --database=ali
# Generate translation files
python manage.py compilemessages

# On website ---------------------
# Create periodic tasks
# Create tracker entry

# create cron job to run certbot every 15 days to update certificates