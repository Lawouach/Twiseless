<!-- -*- markdown -*- -->

Introduction
============
Twiseless aims at providing a demo of the CherryPy framework in its version 3.2.0, demonstrating many aspects of the framework such as:

 * Application serving
 * Static serving
 * Request Tools
 * Engine Plugins
 * Database access
 * Template integration
 * OAuth integration
 
This is list tries to cover the most common usage of CherryPy in a non-trivial yet simple application. Hopefully this will help people making the best of the framework.


Requirements
============

This demo has the following dependencies:

 * CherryPy 3.2.0 (yeah well duh!)
 * Mako
 * SQLAlchemy
 * python-oauth2
 * python-dateutil

You can install them via easy_install|distribute|pip as your environment allows.

OAuth Requirements
------------------

This demo uses the Twitter API to fetch data, this means you must create a twitter application to get a consumer key and secret token. So please go ahead and create a dummy app at https://dev.twitter.com/. You will be required to input the base URL of your app, which will likely be running on your local machine. Use http://127.0.0.1:8090 since http://localhost:8090 will not be permitted.


Overview
========

Twiseless is a useless twitter application, hence the exciting name. It does one single thing, it shows you a pie chart of the people that mentions you the most. Exhilarating, isn't it?

The process followed by Twiseless is as follow:

 * When you go to the home page, if you aren't logged in, it redirects you to the Twitter OAuth page for you to allow the application.
 * Once that's done, you are redirected back to the home page where it shows you the pie chart.

The pie chart is not generated directly from data returned by twitter's API. Instead, a background task asks those data preiodically and fills a local database up. The pie is created from that dataset. This explains why at the beginning you will not see data until the first iteration of the task has completed.

Get Started
===========

 * Install all the dependencies
 * Get a OAuth consumer key and secret tokens for a dummy application with twitter.
   * Update the `conf/app.cfg` file with the key and secret tokens.
 * Start the server:
 `$ python serve.py`
 * Go to http://localhost:8090 and login.

Architecture
============

The goal of this demo is to show how CherryPy's design can help you architecturing your own web application.

Plugin
------

In CherryPy applications are managed by its engine which takes care of hosting them as well as serving them via a dispatcher that maps the request URL to the appropriate controller (also called page handler).

The engine conducts that little world but offers you an API to extend it. These extensions do not participate to the request processing, but instead act globally on the engine instance. What this means is that you can add functions that your application can use at any point whilst the engine is alive. This is the right place whenever you need functions that are not bound to a particular request's state.

Twiseless comes with a few plugins:

 * db: 
   * Manages the database connection, in this case provided by SQLAlchemy
   * Binds a session to the current active thread anytime it is required
 * template:
   * Initiates the templating engine, here Mako
   * Retrieves a template by its name
 * oauth:
   * Provides a mean to create a consumer and a token objects
   * Makes a client request to a OAuth provider
 * twitter:
   * Manages background tasks that fetch data using the twitter API
   * Feeds the local database with fetched data
   
As you can notice, those plugins provide functions to perform operations independantly from any request, though they'll likely be called from a request processing of course.
   
Tools
-----

Tools are more commonly used as they are more easily understood. Tools provide a mechanism to operate on the request's state during its processing. This allows the developer to define behaviors based on the current context.

Twiseless comes with the folowing tools:

 * db:
   * Associates the database session with the current request so that the controller has a db access
   * Commits the associated request when the request's processing terminates
 * template:
   * Renders a template with the data returned by the controller
 * user:
   * If a user is currently connected, retrieves its profile from the local database and attaches it to the request. Otherwise, redirects to the login page.
   
Hopefully it is clear here that those functions are meaningful in the context of the request processing, hence the tools.

Freedom and convenience
-----------------------

CherryPy tries hard not to force you into a specific design like some other frameworks. This has the advantage of giving you more control and a free hand to adapt during development but the drawback obviously is that you need to write some common code yourself. However once you'll have your own setup, you'll probably reuse a lot and, perhaps, package your common tools and plugins into their own specific package.

Design
======

Twiseless doesn't actually come with a very complex application, instead it focuses on the common tools and plugins and the way they can help your design by abstracting away those common functions.

Directory Layout
----------------

Unlike some other large frameworks, CherryPy does not provide you with a script to initiate a project layout which means it's up for you to decide based on your project's goals. Twiseless offers one possible layout:

 * webapp: CherryPy applications in modules
 * template: Mako templates to render into HTML
 * public: static files such as Javascript, CSS, etc.
 * logs: access and error log files
 * lib: any application modules that support the application
 * conf: server and application settings
 
This layout is rather common and provides a clear message. You would probably add a test directory.

Main Entry Point
----------------

In a CherryPy application, your main entry point will quite likely be a module that initialises your plugins, tools, applications and starts the server and engine. In Twiseless, these actions are contained in the top-level `serve.py` module. 

CherryPy application
--------------------

Obviously, what you really want is to serve some application, meaning you need to write some CherryPy aware application. Usually this is done by creating a class that contains methods decorated with `cherrypy.expose`. That decorator sets the `exposed` attribute to `True` on the method it wraps, telling CherryPy that it can take part of matching of a URL's path.





