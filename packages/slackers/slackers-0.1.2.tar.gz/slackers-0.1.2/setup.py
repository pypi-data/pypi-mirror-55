# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['slackers']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.42,<0.43',
 'pyee>=6.0,<7.0',
 'python-multipart>=0.0.5,<0.0.6',
 'requests>=2.22,<3.0']

setup_kwargs = {
    'name': 'slackers',
    'version': '0.1.2',
    'description': 'Slack interaction webhooks served by FastAPI',
    'long_description': '# Slackers\n\nSlackers is a FastAPI implementation to handle Slack interactions.  \n## Installation\nYou can install Slackers with pip\n`$ pip install slackers`\n\n## Configuration\n### `SLACK_SIGNING_SECRET`\nYou must configure the slack signing secret. This will be used to \nverify the incoming requests signature.   \n`$ export SLACK_SIGNING_SECRET=your_slack_signing_secret`\n\n## Example usage\nSlackers will listen for activity from the Events API on `/events`, for\ninteractive components on `/actions` and for slash commands on `/commands`.\nWhen an interaction is received, it will send an event. You can listen\nfor these events as shown in the following examples.\n\n```python\nimport logging\n\nfrom slackers.hooks import actions, commands, events\nfrom slackers.server import api\n\nlog = logging.getLogger(__name__)\n\n@events.on("app_mention")\ndef handle_mention(payload):\n    log.info("App was mentioned.")\n    log.debug(payload)\n\n\n@actions.on("block_actions")\ndef handle_action(payload):\n    log.info("Action started.")\n    log.debug(payload)\n\n@actions.on("block_actions:action_id")\ndef handle_action_by_id(payload):\n    log.info("Action started.")\n    log.debug(payload)\n\n\n@actions.on("block_actions:callback_id")\ndef handle_action_by_callback_id(payload):\n    log.info(f"Action started.")\n    log.debug(payload)\n\n\n@commands.on("foo")  # responds to "/foo"  \ndef handle_command(payload):\n    log.info("Command received")\n    log.debug(payload)\n\n\napp = api\n```\n\nOr, if you already have an API running, you can add slackers as a router\n```python\nfrom fastapi import FastAPI\nfrom slackers.server import router as slack_router\n\n...\n\nmy_app = FastAPI()\nmy_app.include_router(slack_router, prefix="/slack")\n```\n',
    'author': 'Niels van Huijstee',
    'author_email': 'niels@huijs.net',
    'url': 'https://github.com/uhavin/slackers',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
