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

One LSTM layer with 1024 nodes trained on about 5000 batches of size 128

### Tolkien

    Tera II
    Relagir
    Balch-king of Angmar
    Aoedt Gracegirdle
    Foran
    Falring
    Lrgaeg
    Arphr
    Ddreil II
    Hmarsnth Brandybuck
    Aallmir
    Flrg
    Gobae Cotton
    Ilulmur
    Balm Hammerhand
    Garimndo
    Totm
    Glrendil
    Nárian
    Torgo Boffin

### George Martin

    Uyon Tannister
    Aonn lBolton
    Ahmelle
    Mnsiy
    Bonnna Lannister
    Ayonon Poole
    Radelyn Styft
    Jisnel Stlmy
    Gevyne
    Pernin
    Lorras Harlaw
    Ownen
    Aodnor Velaryon
    Glhe Blacken
    Wmrch H Harlaw
    Lbbert Caswell
    Myldssa Florent
    Ltrelle
    Bssyn
    Woyne Marry

### Robert Jordan

    Damelle Arovni
    Jakrn Shaeren
    Dattri
    Aoiiis
    Ddathera Aelfdene Casmir Lounault
    Simril Ondin
    Tarnen
    Vardelain
    Sonarn
    Ehana
    Tamind Anshar
    Eaedeuin
    Rarlin
    Aaulp
    Cenrr e Jaarde
    Fldii
    Arelsrin
    Aiiaael
    Casaa
    Fanlnca Hasad

### Steven Erikson

    Cyry
    Guptan Throe
    Tiindit Purrble
    JeraThuran
    Renu
    Lnarcipor Reese
    Haicman
    Dakao Trumb
    Gefh'Dener
    Glirlas Dnnda
    Tangl
    Blkdan
    Sararchar
    Bether
    Redtron
    Raorl
    Lcarv
    Aet'er
    Enreëor
    Hponcipor Reese

### Brian Jacques

    RaobeuSpinney
    Yhmel
    Bertssckt Siifurd
    Dovftar Brookback
    Blaggoail
    Kister Natena
    Grunkeose
    Faotoe
    Erucjeg
    Sabtmee
    Frother Eerdale
    Uiskie
    Poplurook the Wanderer
    Sizg
    Wonga
    Fenbuck
    Eouncane
    Beirl
    DreFleck
    Sumga

### Frank Herbert

    Cogvoa
    Tanein Frur
    Ciuillo
    Rgeaun Gcru
    Hlee
    Forcy
    Cutise
    Luqif
    Svkis  Daruino II
    Smharl Cdreides
    Legunza Thorvald
    Jllxas
    Ertane Bolitle
    Halbarassa
    Maglr
    Car
    Lasifr Corrino
    Clrrsta
    Klplssa
    Firin

### Andrzej Sapkowski

    Vainfr
    Altckammer
    Fimille
    Biimaana Fichelet
    Aosnis Cranmer
    Ayo Bucnarit
    Vractrrga
    Iuvnidam
    Eonqueline
    Piaiu
    Ahnlgi
    Masko Bruys
    Serengci  Hofmeier
    Dammort Stammelford
    Leineman
    Sdbades Fierabras
    Prifcin of Temeria
    Yddegast
    Racielion
    Hhefli