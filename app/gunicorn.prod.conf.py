# Django WSGI application path in pattern MODULE_NAME:VARIABLE_NAME
wsgi_app = "core.wsgi:application"

# The server socket
bind = "0.0.0.0:8000"
workers = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Timeouts
timeout = 30  # Timeout for worker processes
graceful_timeout = 30  # Time to allow requests to finish after timeout

# Performance Tuning
worker_class = 'sync'  # 'sync', 'async', 'gevent', etc.
worker_connections = 1000  # Max simultaneous clients, relevant for async workers

# Redirect stdout/stderr to log file
capture_output = True

# PID file so you can easily fetch process ID
# pidfile = "/var/run/gunicorn/dev.pid"

# Write access and error info to /var/log
# accesslog = errorlog = "/var/log/gunicorn/dev.log"

# Restart workers when code changes (development only!)
# reload = True