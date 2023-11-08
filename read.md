#  Advice GPT ver 1.0.0-alpha
***
***
Develop a web app that analyses the sentiment given an input and gives an answer personifying a character. The purpose is to emulate as well as possible the character with the given prompts. Additionally, it provides the number of tokens used, well-being level and emotions for tracking and log purposes. Besides, It includes authentication with Mysql and a cute error handler.
The project still requires a lot of work and improvement, you may find that the app still lacks some obvious features as the
profile page for updated information or more...

I struggled the most with things I shouldn't have struggled with. Anyway, I hope you find it helpful



Made by Richi

![Image text](./static/assets/home_page_2.png)


**This project was developed as final project for the CS50x course.**
_Developed with Flask and LangChain (LLM Library)._ 



## Instalation Instructions


1. Get repository: `git clone https://github.com/RIcki-cpu/cs50-finalproject.git`
2. Go to directory: `cd project_directory`
3. Create a virtual enviroment with `python -m virtualenv venv`
    - Activate virtual enviroment `venv\Scripts\activate`
4. Install all requirements and packages: `pip install -r requirements.txt`
5. Install Mysql and restore advicegpt_db database with the files located in mysql directory
    - Recomendation: Mount a container with mysql + phpmyadmin with the docker file within project directory
6. Get your OPENAI_API_KEY with the link and create an account (https://openai.com). The API should start like this...  sk-sjFSJs...
7. Create a .txt file in the project root directory and copy the OPENAI_API_KEY inside the text file
8. Run the project `Flask run` or `python ./app.py`
9. Open Localhost http://127.0.0.1:5001/


## How to use this Project:

1. This project implements Authentication with Mysql
    - Register
        _The password will be encrypted so that ensures security_
    - Log in
    - _Update Profile(planned next update)_

2. This projects implements two routes for Registered users : Home and Emotions Tracker

    - 2.1: **Home page**: Write your feelings, choose your parameters and the app must respond accordingly
    _Note: The emotions and well_being_level would be tracked and stored in the database_

    - 2.2 **Emotions Tracker**: Here you can check your well_being history throughtout time and also see the number of tokens used 

## ScreenShots

![Image text](./static/assets/home_page.png)
![Image text](./static/assets/tracker.png)
![Image text](./static/assets/Sigin.png)
![Image text](./static/assets/register.png)

* _The prompts can be improved and added with  in the file `prompt_templates.py`_



*Thanks for your time 😁*

## FAQs
* Is this the final version?
 - Definitively NOPE, It's the 1.0.0-alpha version

* Is AdviceGPT bug free ?
 - No, The most common bugs and issues must have been solved, but some still remain

* I've got suggestions, what should I do?
 - Any suggestions, please don't hesitate to ask for or even contribute to the project. I'm still sort a beginner in this

* What feature do you plan to add to the future ?
 - Improve UX
 - Add profile Page
 - Add more characters to the prompts
 - Limit Token usage
 - Add charts to the Tracker Page
 - Fix some bugs
 - Improve the perfomance of the prompts
  ... to mention some of the main ideas


***