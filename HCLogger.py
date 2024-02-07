import json
import datetime
import websocket

# Replace 'wss://hack.chat/chat-ws' with the actual WebSocket URL
ws = websocket.create_connection('wss://hack.chat/chat-ws')

# Bot configuration
nick = 'NotALogger'
channel_to_join = 'programming'
password = '<your_password>'  # Set a password if required

# Join the specified channel with the given nickname and password
join_cmd = {
    'cmd': 'join',
    'channel': channel_to_join,
    'nick': nick,
    'pass': password
}
ws.send(json.dumps(join_cmd))

# Main loop
while True:
    result = json.loads(ws.recv())

    # Process and log the message
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if 'cmd' in result:
        if result['cmd'] == 'onlineAdd':
            # 'onlineAdd' event
            nick = result.get('nick', 'Unknown')
            trip = result.get('trip', 'Unknown')
            channel = result.get('channel', 'Unknown')
            user_id = result.get('userid', 'Unknown')
            level = result.get('level', 'Unknown')

            message = f"**{current_time}** - *{nick}* ({trip}) has joined *{channel}* (User ID: {user_id}, Level: {level}).\n"
        elif result['cmd'] == 'chat':
            # 'chat' event
            nick = result.get('nick', 'Unknown')
            trip = result.get('trip', 'Unknown')
            text = result.get('text', 'Unknown')
            channel = result.get('channel', 'Unknown')

            message = f"**{current_time}** - *{nick}* ({trip}) in *{channel}*: {text}\n"
        else:
            # Unknown event
            message = f"**{current_time}** - Unknown event: {result}\n"
    else:
        # Unknown format
        message = f"**{current_time}** - Unknown format: {result}\n"

    # Log the message to a Markdown file (append mode)
    with open('chatlog.md', 'a') as log_file:
        log_file.write(message)
