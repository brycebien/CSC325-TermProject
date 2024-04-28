# Welcome to our Spotify Recommendation App!
## Getting Started

IMPORTANT NOTE: You must send your email address to the developer in order to access the app, because it is still in Spotify's "Develop Mode" and users must be approved before using the Spotify API. Send your information to ajoneal02@gmail.com to get added to the list of approved users. If you are Dr. Zhou grading this project, I have provided a test user account for you to use in the comments of our submission.

### Running locally

1. First, clone the respository

2. Next, you will need a .env.local file. You can either set this up with your own Spotify API client ID and secret. If you are Dr. Zhou grading this project for CSC325, I have included a .env.local file for you in our submission for you to use. The format for the file is:
> SPOTIFY_CLIENT_ID=spotifyclientid

> SPOTIFY_SECRET=spotifysecret

> JWT_SECRET=secretencodingstring

> NEXTAUTH_URL=http://localhost:3000/

3. Make sure you have next.js installed, refer to the [official documentation](https://nextjs.org/docs/getting-started/installation) for installation instructions.

4. Install the correct python libraries using pip install:
> pip install joblib pandas Flask flask-cors

5. Run the Python server by running the 'userInput.py' file
   
6. In different terminal from where the Python server is running, navigate to the root folder of Amassify

7. Run the following commands:

> npm install

> npm run build

> npm run start

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.
