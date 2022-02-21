# External chat connectivity example

This repository contains example application to illustrate how to connect external chat service into Giosg platform.

You can find related tutorial from [Giosg For Developers Documentation](https://docs.giosg.com/tutorials/messaging/external_visitor_chat/).


# Requirements and installation
This project requires Python 3.8+, virtualenv and pip.

1. Clone this repository: `git clone https://github.com/giosg/ext-chat-connectivity-example.git`
2. Make virtualenv and activate it: `mkvirtualenv ext-chat-connectivity-example --python=~/.pyenv/versions/3.8.0/bin/python`
3. Install Python requirements: `pip install -r requirements.txt`
4. Run database migrations: `./manage.py migrate`
5. Start development server `./manage.py runserver`. Test that it can be accessed in `http://localhost:8000`

You will also need to have publicly accessible domain for the application if you want to receive webhooks from Giosg platform. You can use [Ngrok](https://ngrok.com/) for that or you may deploy this app to some cloud host or vps.


# What does this project do and how does it work
Refer to tutorial in [Giosg For Developers Documentation](https://docs.giosg.com/tutorials/messaging/external_visitor_chat/) site to learn more how this project works.