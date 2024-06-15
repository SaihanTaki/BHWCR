# **Bangla Handwritten Character Recognizer**

This is a web app that can recognize bangla handwritten characters. Recognition task is done by using a fine tuned convolutional neural network model.

<a href="https://bhwcr.onrender.com/"> Click here to see live demo </a> <br>
This web app may take upto a minute to load. Pease waite a little bit.

<br>

# **Table of Contents**

-   [Technologies](#Technologies)
-   [Screen Capture](#Screen-Capture)
-   [Model Architecture](#Model-Architecture)
-   [How to run this app](#How-to-run-this-app)
-   [Dataset Source](#Dataset-Source)

<br>

# **Technologies**

-   Tensorflow
-   Keras
-   Python
-   Flask
-   HTML
-   CSS
-   Javascript


<br>

# **Screen Capture**

<img src="static/bangla-char-recog.gif" width="600"/>

<br>

# **Model Architecture**

<img src="static/model_architechture.png" width="600"/>

<br>

# **How to run this app**

-   Create a project directory in your local machine
-   cd to the project directory
-   Run the command in your shell to clone the repo or simply download the zip file

```
$ git clone https://github.com/SaihanTaki/Bangla-Character-Recognition.git
$ cd Bangla-Character-Recognition
```

-   Create a virtual environment
-   Activate the virtual environment
-   Install the dependency by running the following command

```
$ pip install -r requirements.txt
```
-   Run the application using the following command
```
Flask run 
```

Or 

```
gunicorn --bind 0.0.0.0:5000 app:app
```

#### N.B. `Flask run` will start the application in development mode.


<br>

# **Dataset Source**

<a href="https://shahariarrabby.github.io/ekush/#home"> Ekush Dataset </a>
