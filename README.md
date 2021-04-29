# pgUI
Small GUI for pygame.

## Motivation
This repository is for a small GUI to be used along with pygame (graphics python library). 

Python is a great programming language, and pygame an excellent library to -graphically- show whatever you want. While primarily intended for games, it has revealed as a general purpose graphics library. At EIDE foundation is widely used for app's having graphical output.

![](https://user-images.githubusercontent.com/64075009/116436815-100a7100-a84d-11eb-9726-16c61c2997ea.png)

EGR traffic model (PLC training).

Pygame has no interface tools -in a way it is an interface itself. But app's developped on pygame sometimes need one or two buttons to change something. Sometimes they need to show a statistic or a text column ... May be even games sometimes need a button.

pgUI is a pygame 'sub-library' that gives the user the possibility of adding functional buttons and simple texts (both fixed or dynamic -game/app dependant) to your pygame app.

![](https://user-images.githubusercontent.com/64075009/116439558-fb7ba800-a84f-11eb-851b-1dc763527f5c.png)

Chimp game with text added by using pgUI.

## Quick start.
pgUI has been conceived to be used with a minimum of effort. Please, follow the next steps.

### 1.- Download the file pgUI.py.
Basic use of pgUI needs only the file 'pgUI.py': either copy-paste it or download it to your working directory.

### 2.- Example: adding a fixed text.
#### 2.1.- Import module.
Add the 'import' command to your program
    import pgUI as UI

#### 2.2.- Instance a pgUI user.
    UIUser = UI.user(screen)                               
'screen' being the pygame window name in your program. This line of code will give access to all the pgUI module resources.

#### 2.3.- Add a the text you want to be shown.
    UIUser.addInfoText(position = (160, 35),                
                       text = "Chimp says: 'Hello world!'",
                       colors = [(250,0,0), (255,255,255)])
this line will force the text "Chimp says: 'Hello world!'" to unconditionally appear at coordinates (160, 35); 'colors' first member is the text color while second color is the background for the text (normally choosen as the game background color).


