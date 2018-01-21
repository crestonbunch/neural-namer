# Neural Namer

A character RNN that learns how to emulate the styles of names of different
fantasy authors.

Usage
=====

Recommended process is to setup a Python Virtual environment.

First time setup
----------------

This will create a Python virtual environment, and install the necessary
packages only for this project.

    $ pip install virtualenv
    $ virtualenv -p /usr/bin/python3 venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ python setup.py develop

Running from the virtual environment
------------------------------------

Make sure you run the commands from inside the virtual environment, once the
virtual environment is created, you can enter it with:

    $ source venv/bin/activate

Scrape data
-----------

    $ crawl wikia --out crawler/wikia/data/names.csv

Train the model
---------------

    $ model train --data preprocessor/data/vectors.pkl --save modeler/logs/1

Generate names
--------------

    $ model gen --data preprocessor/data/vectors.pkl \
                --lookup preprocessor/data/lookup.pkl \
                --save modeler/logs/1 \
                --author "Tolkien"

Replace 'Tolkien' with another author:

* Tolkien (Lord of the Rings)
* George Martin (A Song of Ice and Fire)
* Robert Jordan (Wheel of Time)
* Steven Erikson (Malazan)
* Brian Jacques (Redwall)
* Frank Herbert (Dune)
* Andrzej Sapkowski (The Witcher)

Unfinished work
===============

* Collect more training data
* Create a web interface
* Explore alternative models

Example output
==============

### Tolkien

    Sabgana
    Twor
    Phingol
    Thorondir
    Harlat
    Imrahil
    Atanatar II
    Bars
    Faramir
    Tar-Vanimeldë
    Gilfanon
    Laurc Baggins
    Elbhir
    Golmberry
    Falco Chubb-Baggins
    Bosco Boffin
    Drogo Baggins
    Arveleg I
    Amlaith
    Celegorm

### George Martin

    Doger Corne
    Jon Mooton
    Yareth II Gardener
    Waymar Royce
    Harry Rivers
    Langor Llegane
    Steffon Stackspear
    Tytos Lannister
    Doreah
    Morrec
    Lina Tyrell
    Indrew Locke
    Walderan Tarbeck
    Lyonel Frey
    Ashera Mallister
    Hobb
    Ryman Frey
    Imry Florent
    Benjicot Blackwood
    Bess Bracken

### Robert Jordan

    Emilyn Arganya
    Kari Thane
    Erac
    Tylamana
    Mirane Larinen
    Kiam Lopiang
    Mevarin
    Malindhe
    Alvon
    Elenar
    Corile
    Setsuko
    Loidelan
    Gaigal Barara
    Jaechim Carridin
    Poranala
    Merean Redhill
    Anvila
    Lisandre
    Jaim Aybara

### Steven Erikson

    Unvathana
    Bowl
    Rival
    Kedranle
    Rogel
    Bester
    Hordilo Stinq
    Tront
    Sevara
    Sheala
    Unk
    Sekara
    Hurta Stinq
    Enesthila
    Barack
    Kalsor
    Erdast Brid
    Stoop
    Lane
    Arba

### Brian Jacques

    Gilly
    Brather Karryw
    Thurdale
    Melko
    Mariel Gullwhacker
    Toobles
    Diiger
    Durby Furrel
    Burrem
    Nutclaw
    Clarissa
    Droppaw
    Brink Greyspoke
    Gullger
    Rankacul
    Boal
    Martin the Warrior
    Ranguvar Foeseeker
    Hookfin
    Ruggan Bor

### Frank Herbert

    Fabiin Corrino
    Gimin Fenring
    Claude Jozziny
    Sheeana Brugh
    Whisicka Corrino
    Geoff
    Hivar Sen Ajidica
    Bital
    Mesa Ecaz
    Windhal Corrino III
    Bhek Tenring
    Tyros Reffa
    Alia Atreides
    Antine
    Doris Bhrazen
    Wellington Yueh/DE
    Tosia Obregah-Xo
    Germon Tero
    Lutier Corrino II
    Spite Blis

### Andrzej Sapkowski

    Amdario Bach
    Echel Traighlethan
    Donimir of Troy
    Jocco Held
    Ovo Mirce
    Vinesne
    Xyhal Pratt
    Marilka
    Tazie
    Drofuss
    Yuzzing
    Patett
    Hithle
    Helmis Farrowtauserithe
    Radovid III
    Tarolina Roberta
    Willem
    Yavvina
    Nozorn
    Carthia van Canten