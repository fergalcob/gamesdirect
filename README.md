![Am-I-Responsive](README/amiresponsive.png)

# Live Link
[https://gamedb-live.herokuapp.com/catalog/](https://gamedb-live.herokuapp.com/catalog/)

## Table of Contents

- [App Goals](#app-goals)
- [Site Strategy](#site-strategy)
  * [Targeted Users](#targeted-users)
  * [Site Goals](#site-goals)
  * [Project Goals](#project-goals)
- [Development Methodology](#development-methodology)
  * [Initial Project Creation](#initial-project-creation)
  * [User Management](#user-management)
  * [Project Data](#project-data)
  * [Wishlists](#wishlists)
  * [Newsletter Subscriptions](#newsletter-subscriptions)
  * [Cart Functionality](#cart-functionality)
  * [Checkout Functionality](#checkout-functionality)
  * [Site Responsiveness](#site-responsiveness)
- [Design Visualization](#design-visualization)
  * [Wireframes](#wireframes)
  * [Database Construction](#database-construction)
- [Features](#features)
  * [Common Features](#common-features)
  * [Home Page](#home-page)
  * [Genre, Developers, Publishers Lists](#genre-developers-publishers-lists)
  * [Search Results, Genre Items, Developer Items, Publisher Items](#search-results-genre-items-developer-items-publisher-items)
  * [Game Description Page](#game-description-page)
  * [Profile Page](#profile-page)
  * [Reviews & Comments](#reviews--comments)
  * [Sign-In, Sign-Up & Password Change Pages](#sign-in-sign-up--password-change-pages)
  * [Profile Update](#profile-update)
  * [My Collections](#my-collections)
  * [Personal Collection](#personal-collection)
  * [Error Pages](#error-pages)
- [Colour Palette](#colour-palette)
- [Typography](#typography)
- [Testing](#testing)
- [Deployment](#deployment)
  * [AWS](#aws)
  * [Heroku](#heroku)
- [Technologies Used](#technologies-used)
  * [Libraries & Frameworks](#libraries--frameworks)
  * [Resources](#resources)
- [Future Improvements](#future-improvements)
- [Acknowledgements](#acknowledgements)


## App Goals

GamesDirect is a primarily Django based project, part of the Code Institute Project Portfolio 5. The aim of this site is to allow users with an interest in gaming a storefront to purchase games from a number of the current most popular platforms. I have integrated this project with both Stripe and Mailchimp to enhance the e-commerce offerings available through the site via newsletters and allowing for direct purchases to be made through the storefront using Stripe Checkout.

### Site Strategy

#### Targeted Users

* Users with an interest in gaming

* Users who would be interested primarily in purchasing digital content in place of physical games

* Users who would be regularly returning to the site to check for new products/items on sale

#### Site Goals

* For users to be able to create an account for themselves

* For users to be able to create a wishlist for themselves to encourage return visits to the site

* To provide up to date information to users when they access the site

* To give users further information when not browsing the site via a site newsletter containing offers, updates, etc.

#### Project Goals

To provide a storefront to users providing digital download keys to gaming focused users. To encourage repeat interactions with the site, regular sales would be implemented which are clearly indicated to the user when viewing the products available on the site.

To implement full CRUD functionality which is accessible to standard users accessing the site normally in addition to superusers through the admin site

### Development Methodology

The project was developed using an Agile methodology with a number of Epics in place and the User Stories arising from them. These User Stories and Epics were kept track of in the Github Project Board found [here](https://github.com/users/fergalcob/projects/2). The following User Stories and Epics were expanded upon within the project board to encompass the tasks that would need to take place to accomplish them:

#### Initial Project Creation

* As a developer I need to be able to set up and create a new Django app before continuing
* As a developer I need to have a Minimum Viable Product to continue development
* As a developer I need to be able to set up and create a new Django app before continuing

#### User Management

* As a user I want to be able to create an account via the site
* As a user I want to be able to log in to the website
* As a user I want my email address to be verifiable for additional security
* As a user I want to be able to reset/change my password
* As a user I want to be able to change my email address if necessary

#### Project Data

* As a developer I want to have specific models in place to hold data for use in project
* As a developer I want to have a dataset for use by users to the site
* As a user I want to be able to find games released on a specific platform
* As a user I want to be able to search for specific products on the site
* As a user I want to be able to search and filter within the products displayed
* As a user I want to be able to view additional information regarding specific products

#### Wishlists

* As a developer I need to be able to store user wishlists for future visibility
* As a user I want to be able to view my wishlist at any time
* As a user I want to be able to add items to my wishlist when browsing the site
* As a user I want to be able to remove items from my wishlist when browsing the site

#### Newsletter Subscriptions

* As a developer I need to set up a Mailchimp account for Marketing API functionality to be used
* As a user I want to be able to sign up for a newsletter through the site

#### Cart Functionality

* As a developer I need to be able to store the items that are added to a users cart
* As a user I want to be able to add items to my cart when browsing the site
* As a user I want to be able to update the quantity of items for a specific product in my cart
* As a user I want to be able to remove items from my cart directly

#### Checkout Functionality

* As a developer I want to have a payment processor in place to handle checkout
* As a user I want to be able to pay for items added to my cart
* As a user I want to be able to know the status of the payment made via Stripe
* As a user I want to be notified of my payment status via email if there are any delays in the payment flow

#### Site Responsiveness

* As a user I will be using the site on a phone and would like it to be easy to use
* As a developer I need to ensure the site is responsive to resolution changes
* As a developer I need to make sure that the content served is appropriate devices

### Design Visualization

#### Wireframes

These wireframes showing the initial concepts for the layout of the site were created using Balsamiq, some of the content structure has changed since their original design but the concepts have remained largely the same.

<details>
  <summary>Index Page - Desktop</summary>
  
  ![Index-Page-Desktop](README/wireframe_index_desktop.png)
  
</details>

<details>
  <summary>Index Page - Mobile</summary>
  
  ![Index-Page-Mobile](README/wireframe_home_mobile.png)
  
</details>

<details>
  <summary>Game Description Page - Desktop</summary>
  
  ![Game-Description-Desktop](README/wireframe_game_description_desktop.png)
  
</details>

<details>
  <summary>Game Description Page - Mobile</summary>
  
  ![Game-Description-Mobile](README/wireframe_game_description_mobile.png)
  
</details>

<details>
  <summary>Forms Pages(Signin, Register, Password Change, Profile Change) - Desktop</summary>
  
  ![Forms-Pages-Desktop](README/wireframe_forms_desktop.png)
  
</details>

<details>
  <summary>Forms Pages(Signin, Register, Password Change, Profile Change) - Mobile</summary>
  
  ![Forms-Pages-Mobile](README/wireframe_forms_mobile.png)
  
</details>

<details>
  <summary>Alphabetical List Pages(Genres, Developers, Publishers) - Desktop</summary>
  
  ![Alphabetical-Lists-Desktop](README/wireframe_alphabetical_lists_desktop.png)
  
</details>

<details>
  <summary>Alphabetical List Pages(Genres, Developers, Publishers) - Mobile</summary>
  
  ![Alphabetical-Lists-Mobile](README/wireframe_alphabetical_lists_mobile.png)
  
</details>

<details>
  <summary>Search Result Pages(Search Results, Genres, Developers, Publishers) - Desktop</summary>
  
  ![Search-Results-Desktop](README/wireframe_searches_desktop.png)
  
</details>

<details>
  <summary>Search Result Pages(Search Results, Genres, Developers, Publishers) - Mobile</summary>
  
  ![Search-Results-Mobile](README/wireframe_searches_mobile.png)
  
</details>

<details>
  <summary>Profile Page - Desktop</summary>
  
  ![Profile-Desktop](README/wireframe_profile_desktop.png)
  
</details>

<details>
  <summary>Profile Page - Mobile</summary>
  
  ![Profile-Mobile](README/wireframe_profile_mobile.png)
  
</details>

<details>
  <summary>Reviews & Comments Page - Desktop</summary>
  
  ![Reviews-And-Comments-Desktop](README/wireframe_reviews&comments_desktop.png)
  
</details>

<details>
  <summary>Reviews & Comments Page - Mobile</summary>
  
  ![Reviews-And-Comments-Mobile](README/wireframe_reviews&comments_mobile.png)
  
</details>

<details>
  <summary>Collections Overview Page - Desktop</summary>
  
  ![Collections-Overview-Desktop](README/wireframe_collections_overview_desktop.png)
  
</details>

<details>
  <summary>Collections Overview Page - Mobile</summary>
  
  ![Collections-Overview-Mobile](README/wireframe_collections_overview_mobile.png)
  
</details>

<details>
  <summary>Collection Items Page - Desktop</summary>
  
  ![Collection-Items-Desktop](README/wireframe_collections_desktop.png)
  
</details>

<details>
  <summary>Collection Items Page - Mobile</summary>
  
  ![Collection-Items-Mobile](README/wireframe_collections_mobile.png)
  
</details>

#### Database Construction

Graphviz was used to create the following image showing the database structure and the relationships between the created models.
![Database Visualization](README/my_project_visualized.png)

## Features

### Common Features

#### Navbar
![Navbar-Desktop](README/header_desktop.png)
<details>
  <summary>Navbar Mobile Closed & Expanded</summary>
  
  ![Navbar-Mobile-Closed](README/header_mobile_closed.png)![Navbar-Mobile-Expanded](README/header_mobile_expanded.png)
  
</details>

All pages display a fixed navbar that switches to a hamburger style dropdown menu when viewing on lower resolution devices. This navbar contains links to all current main sub-sections and to the homepage. The logo for the site is included on the navbar and stays even when in responsive modes. To prevent the navbar from becoming overcrowded, the Games section and Profile section when logged in both have separate dropdown menus for their own navigation. When a user is not logged in they are are presented with a Sign-In or Sign-Up option for them to create/access their own account. When logged in these options are replaced by the username of the logged in user.

#### Footer

![Footer-Desktop](README/footer_desktop.png)

<details>
  <summary>Footer Mobile</summary>
  
  ![Footer-Mobile-](README/footer_mobile.png)
  
</details>

Currently the footer uses a split row design to differentiate between site content and informational content. Links to the various site pages are contained in one and could in future be used to also contain social media links for the site. The bottom row of the footer currently contains a simple copyright detail for the site itself. With the site links, they display in a separated grid to give space when viewing on larger displays, switching to a column layout on mobile/tablets.

### Home Page

![Recently-Viewed-Desktop](README/recently_viewed_desktop.png)

<details>
  <summary>Recently Viewed Mobile</summary>
  
  ![Recently-Viewed-Mobile](README/recently_viewed_mobile.png)
  
</details>

On a users initial access to the page the first item they will encounter will be the introductory text which gives them an overview of the sites goals. On creation of an account, the logged in user will also be presented with a list of their recently viewed games above this introductory text. 

![General-Layout-Desktop](README/general_layout_desktop.png)

<details>
  <summary>Home Page Body Mobile</summary>
  
  ![General-Layout-Mobile](README/general_layout_mobile.png)
  ![General-Layout-Mobile2](README/general_layout_mobile_continued.png)
  
</details>


For all users they will also be able to see a collection of the most recent reviews left and collections published to the site with links to access the full version of the content selected. 

![Recent-And-Upcoming-Desktop](README/recent_and_upcoming_desktop.png)

<details>
  <summary>Recent & Upcoming Releases Mobile</summary>
  
  ![General-Layout-Mobile3](README/general_layout_mobile_end.png)
  
</details>

Scrolling further down the page they will also be able to see some of the most recently released games and games to be released in the next month which is updated on each visit to the site so as to maintain the most up to date information. On mobile this layout switches to a single column view and reduces the amount of images displayed in the recently viewed, recently released and upcoming image carousels to prevent the images from becoming too small due to the default number displayed on larger devices.

### Genre, Developers, Publishers Lists

![Genre-List-Desktop](README/genre_list_desktop.png)

<details>
  <summary>Game Description Mobile</summary>
  
  ![Genre-List-Mobile](README/genre_list_mobile.png)
  
</details>


These pages provide an alphabetical list of the data available for the sections in question. The alphabetical list at the top of the page links to the specific letter in the page to prevent too much scrolling being needed by the user. After the user selects any of the pages within these sections they will be brought to the item pages described in the following section.

### Search Results, Genre Items, Developer Items, Publisher Items

![Search-Items-Desktop](README/search_items_desktop.png)

<details>
  <summary>Search Items Mobile</summary>
  
  ![Search-Items-Mobile](README/search_items_mobile_end.png)
  
</details>

These above pages follow a similar layout due to their design intent as they are displaying a list of items that the user is searching for depending on their needs. The search results page pulls from the IGDB API and populates the content of the database based on the search while the other pages use the data that has already been retrieved to populate those pages. The search results page will return the thumbnail for the cover of the game searched for along with the name of the game along with a link to its description page. In addition to the previous data, the genre,developer and publisher item pages will also return the average review score for the games present based on user reviews and the total number of reviews that have been left for a game that have been used to calculate that average.

### Game Description Page

![Game-Description-Desktop](README/game_description_desktop.png)

<details>
  <summary>Game Description Mobile</summary>
  
  ![Game-Description-Mobile](README/game_description_mobile.png)
  
</details>

The top half of the page contains all the information on the game the user has selected as seen in the above screenshot. When a user has logged in they also have the option to add the game to their personal collection or to add it to a created collection if they have created any and if the game is already part of a collection/s they will also have the option to remove it from the collection they choose. 


![Reviews-Section-Desktop](README/reviews_section_desktop.png)

<details>
  <summary>Reviews Section Mobile</summary>
  
  ![Reviews-Section-Mobile](README/reviews_section_mobile.png)
  
</details>

Below the game information, any reviews left will be displayed along with the option to display any comments if they have been left on a review. For a logged in user they will also be given the option to leave a review/reply to a comment and in addition to this if a user is already an author of a review/comment they will be given the option to edit/delete that content. If they choose to delete a comment, they will be prompted with a pop-up window asking them to confirm the deletion. If the user chooses to leave a review/comment the form field expands to show the text input fields including the text editor for comments/reviews.

### Profile Page

![Profile-Page-Desktop](README/my_profile_desktop.png)

<details>
  <summary>My Profile Mobile</summary>
  
  ![Profile-Page-Mobile](README/my_profile_mobile.png)
  
</details>


The users profile page contains their current profile information and profile picture if set or the default image if not. From here a user can access the content they've created for the site such as their reviews/comments, lists or personal collection. They can also update their profile picture and have options to update their password and profile data. 

### Reviews & Comments

![Reviews-And-Comments-Desktop](README/reviews_page_desktop.png)

<details>
  <summary>Reviews & Comments Mobile</summary>
  
  ![Reviews-And-Comments-Mobile](README/reviews_and_comments_mobile.png)
  
</details>

This page uses a tabbed display to show any reviews or comments left by a user which can be switched between at will. These tabs show the name along with the link to the game, their rating, comments and title for the content as well. These tables are both set to paginate at 10 items to avoid the page becoming overly long and when on mobile devices the review table collapses to prevent horizontal scrolling.

#### Sign-In, Sign-Up & Password Change Pages

![Forms-Desktop](README/forms_desktop.png)

<details>
  <summary>Forms Pages Mobile</summary>
  
  ![Forms-Pages-Mobile](README/forms_mobile.png)
  
</details>

These pages all use a similar design concept and use the same functionality to process the user data. These forms will advise the user of the requirements for the action they wish to take and will be prompted with error messages if they provide incorrect/invalid data. When being processed they use Django's inbuilt authentication functionality to process these requests and work with the User model to update/create the data for the user.

#### Profile Update

Here the user can update certain information from their profile and have it reflected in their profile page.

#### My Collections

![My-Collections-Desktop](README/my_collections_desktop.png)

<details>
  <summary>My Collections Mobile</summary>
  
  ![My-Collections-Mobile](README/my_collections_mobile.png)
  
</details>

Here a user can see all the collections they have made for the site and create new lists for sharing among users of the site itself. After creating a collection, the collection will be in draft mode until at least one item is contained within the collection at which point a user can choose to publish this to the site itself for others to view. Once published they will also have the option to unpublish it or to delete it fully from the site itself.

#### Personal Collection

![My-Personal-Collection-Desktop](README/my_personal_collection_desktop.png)

<details>
  <summary>My Personal Collection Mobile</summary>
  
  ![My-Personal-Collection-Mobile](README/my_personal_collection_mobile.png)
  
</details>

A user can add games to their own personal collection which is only visible to themselves and the intention is for this to be used by people setting up a backlog or collecting a list of what they own without needing to assign it to a specific collection

#### Error Pages

![403-Desktop](README/403_desktop.png)
![404-Desktop](README/404_desktop.png)

<details>
  <summary>403 Page Mobile</summary>
  
  ![403-Page-Mobile](README/403_mobile.png)
  
</details>

<details>
  <summary>404 Page Mobile</summary>
  
  ![404-Page-Mobile](README/404_mobile.png)
  
</details>

A collection of error pages(404, 500, 503) were created for the site and display when the user encounters the specific issue that the error specifies and they are provided with an error image, an explanation of the issue and a link back to the Homepage of the site.


### Colour Palette

![Colour Palette](README/colours.webp)
For this project I decided on a simple dark colour design with a limited number of colours as shown in the above colour palette. I've avoided using pure black in the header and footer as per Material Design recommendations and using the dark gray #121212 in its place. Similarly I'm using the off-white shade #EEEEEE for the general text in place of pure white. The choices of #1F2933 and #212529 are used in contrast to the general page background colour of #241C2C and help to give a sense of elevation and distinguish between elements.

### Typography

For the Navbar I've chosen to use Bruno Ace SC as a semi-futuristic style of font in keeping with the gaming theme of the website. With the remainder of the content, I've chosen to use Ubuntu Light for the text due to its light and simple nature and readability.

## Testing

The results of all testing performed can be found in the TESTING.md file [here](TESTING.md)

## Deployment

### AWS

#### S3(For Media/Static File Storage)

* As we are using AWS for this project for our media/static files and also for the database, we first need to sign in to our AWS account or sign up if you don't have one which can be done [here](https://portal.aws.amazon.com/billing/signup#/start/email)

* Once logged in, we will also need to create a user in order to give the necessary access permissions for performing tasks which will need to be done in the Identity and Access Management console. They will need to be assigned to a group containing the AmazonS3FullAccess permissions so that they can read and write to the bucket.

* Once the user is created and permissions, access keys will need to be generated for them which can be done from their user page in the IAM console

* Within the S3 console, a new bucket will need to be created with the Block Public Access settings disabled to ensure connectivity

* Once created, it may then be necessary to add additional permissions to the bucket as in the following example:

<details>

<summary>AWS S3 Bucket Permissions</summary>

{
    "Version": "2012-10-17",
    "Id": "Policy1488494182833",
    "Statement": [
        {
            "Sid": "Statement1",
            "Effect": "Allow",
            "Principal": {
                "AWS": "*"
            },
            "Action": [
                "s3:ListBucket",
                "s3:ListBucketVersions",
                "s3:GetBucketLocation",
                "s3:Get*",
                "s3:Put*",
                "s3:DeleteObject"
            ],
            "Resource": [
                "arn:aws:s3:::example-bucket",
                "arn:aws:s3:::example-bucket/*"
            ]
        }
    ]
}

</details>

* Once this has been created, we can take the Access Keys and the bucket URL and set these variables within our project

#### AWS RDS(For Database Management)

* Within AWS, we can also create a database from the RDS console

* Here we choose the type of database(PostgreSQL in this case) and set it up with an admin user and password and also ensure that public access is enabled

* With this done and the database created, we can take the URL and admin details to add to the project

### Heroku

* After signing in to the Heroku Dashboard, choose to create a new app

* Give the new app an available name and choose the appropriate location for the app

* After the creation of the app, in the Deploy tab choose to deploy from Github and connect to your GitHub account if necessary

* In the "Connect to Github" section search for the name of the app you are deploying and choose to connect from the search results

* Before deploying the app, the config variables need to be set up in the Settings tab

* For this project, due to the use of AWS for serving media/static files and also for hosting the database, we need to configure the following vars: AWS_ACCESS_KEY_ID, AWS_DEFAULT_ACL, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, DATABASE_URL, USE_S3, MAILCHIMP_API_KEY, MAILCHIMP_TRANSACTIONAL_API, STRIPE_PUBLISHABLE_KEY & STRIPE_SECRET_KEY to ensure all keys are secure

* Optionally, while still in development DISABLE_COLLECTSTATIC can be set to 1 temporarily to prevent static files from being collected on deployment. When hosting on AWS, it can take some time for this to complete and so this option is not needed on all deployments but be sure to remove or set to 0 when doing the final deployment

* Once this is done, return to the Deploy tab and use the option to Enable Automatic Deployments or manually deploy the chosen project

* Once the deployment is complete, the Open App option can be used to bring you straight to the URL for the site

#### AWS RDS(For Database Management)

* Within AWS, we can also create a database from the RDS console

* Here we choose the type of database(PostgreSQL in this case) and set it up with an admin user and password and also ensure that public access is enabled

* With this done and the database created, we can take the URL and admin details to add to the project

## Technologies Used

[Python](https://www.python.org/) - Main language used in the project for all aspects

[Django](https://www.djangoproject.com/) - Python framework used for developing the application

[HTML](https://en.wikipedia.org/wiki/HTML) - Used for designing all the page content

[CSS](https://en.wikipedia.org/wiki/CSS) - Used for styling content displayed to end users

[Javascript](https://www.javascript.com/) - Used for some of the interactive content and formatting of certain pages

[AWS](https://aws.amazon.com/) - Used for hosting the media & static files and also for hosting the PostgreSQL database

[PostgreSQL](https://www.postgresql.org/) - Used for the model databases

[Diagrams.net](https://www.diagrams.net/) - Used to design the flowchart in the README file

[Heroku](https://www.heroku.com/) - For deploying the finished code

[Gunicorn](https://gunicorn.org/) - Python based HTTP server used in deployment of final code

[Visual Studio Code](https://code.visualstudio.com/) - Used as the IDE in the development of the project

[Github](https://github.com/) - Used for hosting finished code for deployment

[Mailchimp](https://mailchimp.com/) - Used the Marketing and Transactional APIs for handling newsletter and order update emails

[Stripe](https://stripe.com/] - Used for handling the checkout functionality of the site

### Libraries & Frameworks

[Bootstrap](https://getbootstrap.com/) - Used for quicker styling of certain elements

[TinyMCE](https://www.tiny.cloud/) - Allows embedding of rich text editor within content allowing users to style their reviews/comments

[jQuery](https://jquery.com/) - Used for running certain Javascript content to handle cart and wishlist functionality

[Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) - Used to integrate AWS S3 bucket for content upload and retrieval

[Crispy Forms](https://django-crispy-forms.readthedocs.io/en/latest/) - Django library to assist in the rendering of forms within templates

[Django Widget Tweaks](https://pypi.org/project/django-widget-tweaks/) - Used to extend the options available with regards to form fields within templates in order to add attributes

[Pillow](https://pillow.readthedocs.io/en/stable/) - Python image library used for conversion and assignment of image files

[Psycopg2](https://pypi.org/project/psycopg2/) - Python database connector used to connect with PostgreSQL database

[Django Resized](https://pypi.org/project/django-resized/) - Used to resize images for saving to S3 bucket

[DataTables](https://datatables.net/) - jQuery plugin used to paginate the content in the tabbed pages of the My Reviews & Comments page

[Slick](https://kenwheeler.github.io/slick/) - Slider used for image carousels on home page

[Star Rating](https://plugins.krajee.com/star-rating) - jQuery plugin used for the hoverable star rating option when leaving a reviews/comments

[Django After Response](https://pypi.org/project/django-after-response/) - Used to call certain functions after initial response to reduce load times

[Mock](https://mock.readthedocs.io/en/latest/) - Used for simulating file objects to test FileField forms in the tests.py file

### Resources

[Graphviz](https://graphviz.org/) - Used to create the representation of the database structure and its relationships

[Balsamiq](https://balsamiq.cloud/) - Used to create the wireframes made for the outline of the site

[IGDB](https://www.igdb.com/) - API used to retrieve content for initial population of project

[MDN](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django) - Used as tutorial on Django set upload

[CDNFonts](https://www.cdnfonts.com/) - Used for the custom fonts used in the project

[W3Schools](https://www.w3schools.com/python/default.asp) - General documentation on Python syntax

[PyPI](https://pypi.org/) - Used for finding specific Python/Django libraries to meet the project needs

[Django Project Documentation](https://docs.djangoproject.com/en/4.2/) - Useful for clarification on certain aspects of Django commands

## Future Improvements

* Currently the site only supports direct user registration, in future I would like to add social account signups to handle OAuth logins via Gmail, Facebook etc.

## Acknowledgements

The guides [here](https://testdriven.io/blog/django-stripe-tutorial/) and [here](https://testdriven.io/blog/django-mailchimp/) at Testdrive were extremely useful in stepping through the process of setting up both the Stripe and Mailchimp integrations for use in the order handling process of the application.

Thanks as well to [Stack Overflow](https://stackoverflow.com/) for their extensive knowledge on the causes of Python errors and the solutions to them.
