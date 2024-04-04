# cintel-05-cintel
###  Project 5: Interactive App with Continuous Intelligence

In this module, we introduce aspects of continuous intelligence - outputs updated on a regular basis or in real time as information becomes available. We provide only basic examples, but the principles enable a variety of continous intelligence aspects for many types of dashboards. 

You should have already created a project repo named cintel-05-cintel with 4 files: 

README.md
.gitignore
requirements.txt
app.py (OR dashboard/app.py if working locally and deploying to GitHub pages - see more below).
If you decide to try the local development, you'll be able to deploy your live date site using GitHub Pages. To make it easy to build our app from a folder and export the app into the docs folder (for Pages), please move your app.py file into a folder. I named my folder "dashboard", so I have a dashboard/app.py file and no app.py in the root folder. This is a more common organization for Python projects. 

You may develop your app in the browser (recommended if you have NOT had 44-608) or develop your app on your machine locally (recommended if you have had 44-608 and/or prior practice with project virtual environments). 

Your app.py or dashboard/app.py file should have the following sections:

imports (at the top), e.g., shiny, random, datetime
define a reactive calc to fake new data points
define the Shiny Core app_ui
The overall page options
A sidebar
The main section with ui cards, value boxes, and space for grids and charts
Your app should have similar functionality to this basic example before you begin: 

Basic App: https://github.com/denisecase/cintel-05-cintel-basicLinks to an external site.
Once we have live data coming in, we need to want to create temporary storage to hold the "most recent" so we can present that - and analyze it online machine learning algorithms such as predicting a trend line using linear regression. We have a whole course on Streaming Data and another on Machine Learning, so you do NOT need to be able to implement those from scratch. Instead, we want to focus on your skills with presenting and displaying the information that might be available in an accessible and useful manner. 

I will provide an example that includes storing the readings in a deque (of dictionaries) and wrapping that deque in a reactive value as a way to manage our constantly changing state.

Your job is to:

implement the example provided and
propose and implement an enhancement, extension, or variation on the app. 
Options include:

Changing the theme, colors, visuals to be more engaging
Changing the layout to better show the current deque
Changing the chart to not flash on each update
Changing the subject domain from temperatures in Antarctica (so we can add it to our Penguin Dashboards) to an alternate focus using random data appropriate for your chosen domain. 
Integrating live data and continuous intelligence into your own previous interactive app
The goal is to understand the possibilities and challenges of working with live data and consider how you can analyze and present "data in motion" to enhance your analytics projects. 
