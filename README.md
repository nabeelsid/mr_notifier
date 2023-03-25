# MR Notifier

This project is for people explores an idea of having more than one way of notifying a reviewer that there is an MR waiting for them. The approach adopted in this project was to send macOS notification to a reviewer if they are tagged as one. The python script queries the Gitlab API (authorized by access token) to fetch merge request information and sends a notification. Refresh interval to fetch new MR information can be set to user defined values.
#
*You can call it Mister notifier; cuz you know MR as is Mister? It's not cheesy at all*

