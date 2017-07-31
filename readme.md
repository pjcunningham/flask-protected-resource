### Using protected resources (images/css/js) in Flask

Resources are not served from the ```static``` folder. Resources are referenced through protected routes and delivered via Flask's ```send_file``` method. Protected routes are configured to set no browser caching on the response header. 

In this example resources are stored under the Flask ```instance_path``` folder.

Don't forget to set the Flask ```instance_path``` particular to your set-up, for example :

```app = Flask(__name__, instance_path='D:/Paul/Documents/GitHub/flask-protected-resource/instance')```