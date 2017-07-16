# Neural Namer

A character RNN that learns how to emulate the styles of names of different
fantasy authors.

Implemented in TensorFlow with RNN cells based on the following paper:
https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/rnn_ctxt.pdf

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

    $ crawl wikia --out crawler/wikia/data/names.pkl

Preprocess data
---------------

    $ preprocess --in crawler/wikia/data/names.pkl \
                 --out preprocessor/data/vectors.pkl \
                 --lookup preprocessor/data/lookup.pkl

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

* Tolkien
* George Martin
* Robert Jordan
* Steven Erikson
* Brian Jacques
* Frank Herbert

Unfinished work
===============

* Collect more training data
* Create a web interface
* Explore alternative models

Example output
==============

### Tolkien

    Griin
    Arrucda
    Urfaelt
    Firaicth
    Caadbuaurk
    Romie
    Findod
    Waor
    Jareë
    Grlaor
    Carthad G
    Halno
    Zarahoo Boffin
    Harn
    Pelan
    Doera
    Donilatad
    Quillia
    Vardul
    Xilanar

### George Martin

    Daria Lannister
    Corter Prke
    Urrall Bne she Sho's's tarter
    Elsalaene
    Yuun Royce
    Ordy'n
    Aegyon Targaryen
    Elier srontise
    Elyra Snokhare
    Xiro Harlale
    Wanon
    Garla
    Lonnel Rannister
    Hagh Sparrow
    Quentien guarder
    Xicen Taover
    Samlis
    Marchant captain
    Hagh Sriester
    Aeeo

### Robert Jordan

    Hardla
    Falle
    DaranieCapmaai
    Haraai
    Elis aLaudaw
    Janric aegiil
    Innlla Lewin
    Alineal
    Harn
    Larraan
    Waninlla Narencelona
    Darane Larnaak
    Larrid
    Ronaan
    Ron Marwn
    Karhlaa
    Invyn al'Vanr
    Falrnl  Cndhom
    Malaail
    Janii Lollin

### Steven Erikson

    Yulka
    Nelb
    Uru an
    Zailh
    Elaat
    Jaels
    Yullck
    Duligen
    Nerpl
    Dulsemfrce
    Inahrath Godes
    Duasuk Of A'nan
    Jalll
    Wais
    Sallrss
    Xiaaelea
    Talmsk
    Kallin
    Nerpera
    InarhnalSoleeu

### Brian Jacques

    Oreu
    Viglag
    Brother Frngle
    Zaigga
    ViglSl'Caus
    Haoheaw
    Siiger
    Luny Firdatcu
    Duana I
    Turmscotk ail
    Yooker
    NirguSonglawol
    Nirgue
    Grrrl
    TurblMigool
    Jarglg
    Wiibd
    Inil
    Vigl tarissuut
    Vigka Longtooth

### Frank Herbert

    Xirdena Torei
    Harimir Fenring/XDj
    Leto Atreides I
    Ininis a
    Kales Atreides
    Ordm
    Jamoi
    Xirdon Corrino
    Xidd  Cenniuu
    Chali KynesXD
    Marie Botler
    GarliXD
    Maruy
    Duria  Harkonnen
    Alixandrr
    BuuanBhxper
    Virgia Aiallg
    ZanaraTerk
    Gainoos
    Garual Cane