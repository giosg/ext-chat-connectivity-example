# External chat connectivity example

This repository contains example application to illustrate how to connect external chat service into Giosg platform.

You can find related tutorial from [Giosg For Developers Documentation](https://docs.giosg.com/tutorials/messaging/external_visitor_chat/).


# Requirements and installation
This project requires Python 3.8+, virtualenv and pip.

1. Clone this repository: git clone
2. Make virtualenv and activate it: `mkvirtualenv ext-chat-connectivity-example --python=~/.pyenv/versions/3.8.0/bin/python`
3. Install Python requirements: `pip install -r requirements.txt`
4. migrate, start server, test it can be accessed
5. install ngrok for tunneling, test it
6. Start ngrok


# What does this project do and how does it work
1. Giosg app
2. webhooks from giosg
3. Webhooks from external system

# TODO
1. Send chat to Giosg when new webhook gets received
2. Send chat to external system when giosg chat has started
3. Send messages between services
4. Draw diagrams and take screenshots about app creation and installation, setup and dataflow diagram
5. Explain modules in django app
6. Explain ngrok
7. Explain how to see what the webhook payload is