# pure-guestbook
A Guestbook server that doesn't need PHP or CGI or any other external APIs.
How it works is you host your main web server like Apache or Nginx on the same machine as the script, put the frontend code on your website, and in the Python code you can change where you want to store your json. You can change it to your web server's directory or make a seperate server to store the JSON and modify the frontend to a different address. It's super simple to setup.
