# Stops the SIADS 521 dashboard app at 10 PM CST so overnight idle compute
# doesn't burn the Databricks Free Edition fair-usage quota. The 5 AM
# keep-alive job starts it again each morning.
# Runs on a schedule: if the app is RUNNING, stop it; otherwise do nothing.
from databricks.sdk import WorkspaceClient

APP_NAME = 'siads-521-energy-dashboard'

w = WorkspaceClient()
state = w.apps.get(APP_NAME).app_status.state
state = getattr(state, 'value', state) #SDK returns an enum — compare as a string
print(f'{APP_NAME}: {state}')

if state == 'RUNNING':
    w.apps.stop(APP_NAME)
    print(f'stop requested for {APP_NAME}')
else:
    print('not running — nothing to do')