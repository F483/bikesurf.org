============
User Stories
============

The user stories are the basis for the requirements of the site.

.. contents:: Table of Contents


Authentication
==============


Register
--------

User clicks the register button. The register page is loaded where the user 
enters required information. Afterwords the user is sent a email with a link 
to confirm ownership. The is redirected to a page that tells them to click on 
the confirmation link in the email.


Login
-----

A User clicks login button. The login page is loaded and the user prompted for
email and password. After a correct login the user is sent back to the page 
they game from.


Login Required
--------------

The user visits a page that requires the user to be logged in. The login page 
is loaded and the user prompted for email and password. After a correct login 
the user is sent to the page that required the login.


Social Login
------------

The user has the option to login via another site (facebook, twitter, etc ...)
instead of providing an email and password. Registering is no longer required,
if the user does not yet have an account is is simply created.


Logout
------

The user clicks the logout button. If the page the are currently on requires a
logged in user they are sent to the index page, otherwise they remain on the 
current page.


Teams
=====


Create Team 
-----------

User clicks 'create team' in the team list page (only visible if logged in).
Create team page is opened and user can enter team data. When the team has 
been created, the user as automaticly added as a member and redirected to 
the team page.


Edit Team 
---------

A user clicks 'edit team' on the team page (only visible if a team member).
The edit team page is opened where the user can change the team data. When 
the changes have been saved the user is redirected to the team page.


Join Team 
---------

The user clicks 'join team' on the team page (only visible if logged in and 
not a team member). The 'request join team' page opens where the user can 
enter an application text. After submitting the user is redirceted to a page 
which notivies that a request to join the team has been made. 
The team recieves a message that a join request has been made.


Accept/Decline Join Request from Message
----------------------------------------

The 'join requests' page of the team is open with a list of requests showing 
relevant information as well as a 'process request' button.
The 'process request' button is pressed which opens the 'process request' page.
The user can enter a response text and press the 'Accept' or 'Decline' button.
Afterwords the user is redirected to the 'join requests' page.
The user and team recieve a message if the request was accepted or denied.


Accept/Decline Join Request from Team Page
------------------------------------------

The user if viewing a message resulting from a join request being made.
The 'process request' link is clicked which opens the 'process request' page.
The user can enter a response text and press the 'Accept' or 'Decline' button.
Afterwords the user is redirected to the 'join requests' page.
The user and team recieve a message if the request was accepted or denied.


Leave Team 
----------

The user click the 'leave team' button on the team page (only visible if logged 
in and not a team member). The user is removed from the team and redirected to 
the team page. The team recieves a message that the user has left the team.
If the user was the last team member the team is deleted.
TODO what happens with bikes in other team stations etc... ?


Remove User
-----------

TODO


Accept/Decline Remove Request from Message
------------------------------------------

TODO


Accept/Decline Remove Request from Team Page
--------------------------------------------

TODO


Station
=======


Add Station
-----------

TODO


Edit Station
------------

TODO


Remove Station
--------------

TODO


Set Inactive
------------

TODO


Set Active
----------

TODO


User Vacation
=============


Add Vacation
------------

TODO


Remove Vacation
---------------

TODO


Edit Vacation
-------------

TODO


Bikes
=====


Add Bike
--------

TODO


Edit Bike
---------

TODO


Remove Bike
-----------

TODO


Set Inactive
------------

TODO


Set Active
----------

TODO


