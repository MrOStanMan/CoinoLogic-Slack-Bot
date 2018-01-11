
#import os
# import time
# import re
# import json
# from slackclient import SlackClient
# #from flask import Flask, request, make_response, Response

# #Initialize Flask Webserver
# #app = Flask(__name__)

# def parse_bot_commands(slack_events):
#     """
#         Parses a list of events coming from the Slack RTM API to find bot commands.
#         If a bot command is found, this function returns a tuple of command and channel.
#         If its not found, then this function returns None, None.
#     """
#     for event in slack_events:
#         if event["type"] == "message" and not "subtype" in event:
#             user_id, message = parse_direct_mention(event["text"])
#             if user_id == starterbot_id:
#                 return message, event["channel"]
#     return None, None

# def parse_direct_mention(message_text):
#     """
#         Finds a direct mention (a mention that is at the beginning) in message text
#         and returns the user ID which was mentioned. If there is no direct mention, returns None
#     """
#     matches = re.search(MENTION_REGEX, message_text)
#     # the first group contains the username, the second group contains the remaining message
#     return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

# #Route For Server
# #@app.route("/handle_command", methods=["POST"])
# def handle_command(command, channel):
#     """
#         Executes bot command if the command is known
#     """
#     # Default response is help text for the user
#     default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND)

#     # Parse the request payload
#     #form_json = json.loads(request.form["payload"])

#     # Finds and executes the given command, filling in response
#     response = None

#     # This is where you start to implement more commands!
#     if command.startswith(EXAMPLE_COMMAND):
#         response = "Sure...write some more code then I can do that!"  

#     # Get list of users
#     userList = slack_client.api_call(
#          "im.list",
#          token = 'xoxb-291704202337-GuHliRDvXenLZ4lhRN5f5GzV'
#     )

#     # Iterate through userList and send message directly
#     del userList['ims'][0]
#     for user in userList['ims']:
#         answer=slack_client.api_call(
#             "chat.postMessage",
#             #Toms slackbot DM
#             channel= user['user'],
#             as_user = True,
#             text=response or default_response,
#              attachments= [
#                     {
#                 "text": "Stress Range Question",
#                 "fallback": "Oops..You didn't pick a level",
#                 "callback_id": "wopr_game",
#                 "color": "#3AA3E3",
#                 "attachment_type": "default",
#                 "actions": [
#                     {
#                         "name": "1-3",
#                         "text": "1-3",
#                         "type": "button",
#                         "value": "1-3"
#                     },
#                     {
#                         "name": "4-6",
#                         "text": "4-6",
#                         "type": "button",
#                         "value": "4-6"
#                     },
#                     {
#                         "name": "7-10",
#                         "text": "7-10",
#                         "type": "button",
#                         "value": "7-10",
#                     }
#                 ]
#             }
#         ]

#         )

# # instantiate Slack client
# # token should not be instantiated directly this will need to be changed for security purposes
# slack_client = SlackClient('xoxb-291704202337-GuHliRDvXenLZ4lhRN5f5GzV')
# # Flask webserver for incoming traffic from Slack

# # starterbot's user ID in Slack: value is assigned after the bot starts up
# starterbot_id = None
# # constants
# RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
# EXAMPLE_COMMAND = "do"
# MENTION_REGEX = "^<@(|[WU].+)>(.*)"

# if __name__ == "__main__":
#     if slack_client.rtm_connect(with_team_state=False):
#         print("Starter Bot connected and running!")
#         # Read bot's user ID by calling Web API method `auth.test`
#         starterbot_id = slack_client.api_call("auth.test")["user_id"]
#         while True:
#             command, channel = parse_bot_commands(slack_client.rtm_read())
#             if command:
#                 handle_command(command, channel)
#             time.sleep(RTM_READ_DELAY)
#     else:
#         print("Connection failed. Exception traceback printed above.")

from flask import Flask, request, make_response, Response
import os
import json

from slackclient import SlackClient

# Your app's Slack bot user token
# SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
# SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient('xoxb-291704202337-GuHliRDvXenLZ4lhRN5f5GzV')

# Flask webserver for incoming traffic from Slack
app = Flask(__name__)

# Post a message to a channel, asking users if they want to play a game

attachments_json = [
    {
        "fallback": "Upgrade your Slack client to use messages like these.",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "callback_id": "menu_options_2319",
        "actions": [
            {
                "name": "games_list",
                "text": "Pick a game...",
                "type": "select",
                "data_source": "external"
            }
        ]
    }
]


slack_client.api_call(
  "chat.postMessage",
  channel="C8LPBSMBP",
  text="Shall we play a game?",
  attachments=attachments_json
)


@app.route("/slack/message_options", methods=["POST"])
def message_options():
    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    menu_options = {
        "options": [
            {
                "text": "Chess",
                "value": "chess"
            },
            {
                "text": "Global Thermonuclear War",
                "value": "war"
            }
        ]
    }
    return Response(json.dumps(menu_options), mimetype='application/json')


@app.route("/slack/message_actions", methods=["POST"])
def message_actions():

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    # Check to see what the user's selection was and update the message
    selection = form_json["actions"][0]["selected_options"][0]["value"]

    if selection == "war":
        message_text = "The only winning move is not to play.\nHow about a nice game of chess?"
    else:
        message_text = ":horse:"

    response = slack_client.api_call(
      "chat.update",
      channel=form_json["channel"]["id"],
      ts=form_json["message_ts"],
      text=message_text,
      attachments=[]
    )
    return make_response("", 200)

@app.route("/") # take note of this decorator syntax, it's a common pattern
def hello():
    return 

if __name__ == "__main__":
    app.run(port=4390)