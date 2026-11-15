# Keeps the SIADS 521 dashboard app alive on Databricks Free Edition,
# which auto-stops apps 24 hours after their last start/update/deploy.
# Runs on a schedule: if the app isn't RUNNING, start it; otherwise do nothing.
from databricks.sdk import WorkspaceClient

APP_NAME = 'siads-521-energy-dashboard'

w = WorkspaceClient()
state = w.apps.get(APP_NAME).app_status.state
state = getattr(state, 'value', state) #SDK returns an enum — compare as a string
print(f'{APP_NAME}: {state}')

if state in ('RUNNING', 'DEPLOYING'):
    print('already up — nothing to do')
else:
    try:
        w.apps.start(APP_NAME)
        print(f'start requested for {APP_NAME}')
    except Exception as e:
        #benign race: another trigger just started the app
        if 'ACTIVE state' in str(e):
            print('compute already active — nothing to do')
        else:
            raise
