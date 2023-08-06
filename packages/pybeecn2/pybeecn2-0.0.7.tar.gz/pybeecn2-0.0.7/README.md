# PyBEECN2

# Table of Contents

1. [Overview](#overview)
1. [Processes](#processes)
    1. [Setup Requirements](#setup-requirements)
        1. [Environment Setup](#environment-setup)
        1. [For Mac Users](#for-mac-users)
        1. [For Windows Users](#for-windows-users)
    1. [App Installation](#app-installation)
        1. [App Exploration](#app-exploration)
    1. [Usage](#usage)
    1. [Run The App!!](#run-the-app)
    1. [Development](#development)
        1. [Make Your Working Directory](#make-your-working-directory)
        1. [Clone Pybeecn2](#clone-pybeecn2)
    1. [Post Merge Procedures](#post-merge-procedures)
        1. [Uploading the update to PyPi](#uploading-the-update-to-pypi)
1. [Summary](#summary)
1. [Further Collaboration](#further-collaboration)
1. [Useful links if you need additional help!](#useful-links-if-you-need-additional-help)
1. [Data Used](#data-used)

## Overview
This project was developed as an initial effort to look at the number of demographic populations in the City of Portland, 
OR. The purpose for this project was to be used by the Portland Bureau of Emergency Management to understand these 
demographics populations within the sub communities of Portland in order to better support the communities surrounding
Basic Earthquake Emergency Communication Nodes (BEECN) and the community as a whole. The tool that was developed is a commandline
interface tool (CLI) which generates a map of the Portland area and a number of map layers to view the distribution of
different demographic populations throughout the city. The map also allows the user to visualize the BEECN locations on 
the map. 

## Processes
The processes to be able to use the tool are described in the section below

### Setup Requirements
In order to use the tool, a user will need to install a few things on their machine. Depending on what machine you have, 
will result in the necessary steps to take. Regardless, you will need to install a working python environment on your 
machine. To do so, please follow the recommendations below depending on the operating system you are using. The installation
could take several minutes. 

#### Environment Setup
Step 1: Open up a terminal on your machine. 

#### For Mac Users
Step 2: Install and setup Homebrew. Homebrew is used as a package manager on your machine. The package manger will help 
automate the processes of included in installing other development software. To install homebrew, run the following code
in your commandline terminal you have open. 
```bash
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
#### For Windows Users
The original developer for this application is not familiar with the process for setting up a working python environment
for windows operating systems. The recommendation is to consult a developer that is familiar with setting up a working
python environment for windows. Additionally, you may consider consulting 
[ANACONDA FOR PYTHON](https://www.anaconda.com/what-is-anaconda/) for setting up the environment. 

Step 3: Open your bash profile and add text. You will need to add a command to your .bash_profile. To do this, on the 
commandline, run the command (Note: you can use your preferred text editor if you feel commandline savvy):
```bash
nano ~/.bash_profile
```
When the text editor opens up, add the text:
```text
export PATH=/usr/local/bin:$PATH
```

Finally, close the text editor with the 'control x' as indicated on the editor in the lower left. Then type 'Y' to save. After this, 
you will have to 'source' the .bash_profile. To do this, run the following command from the terminal. 
```bash
source ~/.bash_profile
```
Then, verify that Homebrew is ready to use with, 

```bash
brew doctor
```
Step 4: Install Python 3. This will be easiest done with the following command in the commandline terminal.
```bash
brew install python3
```
This command will also install pip, setuptools, and wheel. These are more tools for the development of python tools and 
will be discussed in the following [Development](#development) section in this documentation. 

### App Installation
App installation is quite easy at this point. Simply run the code below;
```bash
pip install pybeecn2
```
After you run this command, you will see a number of things populate in the commandline. The application is installing
any requirements the application is dependent on. It is installing additional python packages that pybeecn2 needs 
in order to run.

#### App Exploration
You may want to explore the application a bit before you use it and to get a little comfortable with using the commandline. 
To do so, run the following command and see what happens!

```bash
pybeecn2 -h
``` 
The -h on the commandline is what is called a flag. By entering this flag after the application name and pressing enter on 
your keyboard, you will populate the commandline window with the help instructions for that level of the application. In
this case, you are shown what the next level command of the application is, which is 'vis'. To see instructions for the next
level of the application, fun the following in the commandline;

```bash
pybeecn2 vis -h
```
This will populate the help instructions for the visualization portion of the application. Again, you will see the subcommands
that belong to this application. Now enter the following to see the instructions for the 'map' level of the application.

```bash
pybeecn2 vis map -h
```
This will populate the commandline window with the map level help instructions for the pybeen2 application. You can see
all of the inputs a user needs to use the map level of the pybeecn2 application. 

### Usage 
Initial usage of the application is limited to the ability to view the distribution of Limited English Speaking 
populations across the City of Portland, OR. In order to use the application, you will need to input a number of commands in the commandline of your
machine. Entering the proper input arguments, will;

1. Create a directory on your machine in the location in which you instruct it to. 
1. Download both BEECN data and Population data that exists on [Portland Open Data](http://gis-pdx.opendata.arcgis.com/)
1. Save a viewable map of both BEECN locations and Population information surrounding the BEECN sites. 
    1. The map file will be saved as an html file and does not require any additional work for the user to veiw. 
    1. The map contains a number of selectable layers for the user to view the different populations and how they 
    are distributed across the City of Portland, OR. 

In the application's current state, it is limited to only being used for the purpose of viewing both the distribution
of the total population of Portland and the distribution of Limited English Speaking Populations. However, given people 
with the right skills to develop the application, it's use could be developed and increased to be used with most or all
of the City of Portland's publicly and privately available data. The instructions for general development of the application
will be described below.

### Run the App!!
Running the app is quite easy at this point! But first, you will need to answer one question.
- Where do you want to save the application?
    - Once you have this figured out, this will be your input for the --directory flag. 

After you determine this, you are ready to put all inputs in the application as follows;
```bash
pybeecn2 vis map --points https://opendata.arcgis.com/datasets/6e6185533d5447deb8b7204c27e1858e_92.geojson
--boundaries https://opendata.arcgis.com/datasets/386fd0d07bca42d09f4fd46462bf8a7d_121.geojson 
--directory ~/your_directory/goes_here
```
Note that you could run the command above as is and the application will create the folder ~/your_directory/goes_here
for you. 

After you run the command, again you will see a number of items populate in the commandline window. This output
is indicating what part the program is running. For example, the last items that are output in the commandline 
window are indicating that the map layers for each Limited English Speaking populations is being made. 

After the application is complete, navigate to the folder that you designated as the directory so you can see the map!
Once you are there the map will be located in the plots folder. Simply double-click the file beginning with 'population_map'. 

Note there are some nuances about the different map. Make sure you only have one map layer selected at a time.
The map opens with displaying the layer with the total distribution of the portland Population, the BEECN sites, 
and a 1600m radius ring around the sites.  The application will also create a few other directories on your machine
for the ability to save more data, plots, or other analysis files in the event you want to further develop the application. 

### Development
Under these instructions, it is assumed that the developer has some familiarity with the git development process and 
has a github or similar account to be able to collaborate on development. 

To develop this application there are a number of things that you will need to do. Assuming that you have gone through 
the initial setup of your python environment, you will now have to setup a location on your machine where you will 
develop the application. To do this is quite easy! Decide where on your machine you will do your development or create 
a new directory with the following command on the commandline;

#### Make Your Working Directory
```bash
mkdir ~/your_development/directory_here/
```
Once you create your desired folder, you will have to navigate to it with;
```bash
cd ~/your_development/directory_here/
```
#### Clone Pybeecn2
Then, you are ready to clone the pybeen2 application onto your machine to develop with;
```bash
git clone https://github.com/glmcbr06/pybeecn2.git
```
Now, you'll have to navigate to the pybeecn2 directory that you just cloned with;

```bash
cd pybeen2
```
You can begin developing the app and your changes will be implemented on your machine immediately after you run the 
following command on your commandline;
```bash
pip install --upgrade --no-deps -e .
```
Congrats! You are now ready to begin developing the application and expanding it's uses!!

To begin developing, use the standard git practices of creating a new branch to work and test your development on by;
```bash
git checkout -b feature/your_feature
```
Think of how you would like to expand the use of the application, create your branch to work on, make some changes, and
see the improvements on your machine! When you are ready for the changes to be distributed to the master branch, you will
need to do a few things. You will need to add the new code to git, commit the code, and push the branch to the remote 
repository located on github. Not much work is required here by the developer!!

Run the following to add the new changes/new files you have created;
```bash
git add [file with new code here]
```
Don't worry, if you do not do this properly, git will prompt you with some recommendations in the commandline. 
Then,
```bash
git commit -m "Some comments about this commit and changes/additions you are making"
```
Again, if you mess this up a bit git will prompt you with some recommendations. 

Finally,
```bash
git push
```
After this, git will prompt you to set the upstream location if it is not already set. Simply copy the upstream 
location and run the command again with addition of prompted upstream location;

```bash
git push [prompted upstream location here]
```
Now when you make new changes and want to commit and push them you will simply be able to run git push from the commandline
when you are ready. 

When your new feature is in working order it is ready to merge into the master branch! Navigate to your branch on github
and create a merge request and begin the code review process. 

### Post Merge Procedures
The application is published to the PyPi package repository for easy distribution. The app will also need to be updated
there once branches have been merged into the master branch. This process assumes that the developer has installed 
and setup necessary PyPi and Github (or other version control) accounts in order to develop and maintain a distribution
of the application. 

#### Uploading the update to PyPi
To keep the distribution of the application up to date you will have to do a few additional things. 

Step 1: you will have to update the version number of the distribution. In whatever text editor you are using for 
development, navigate to 'setup.py'. In setuptools.setup, you will find version=x.x.x. Update the version number
to the appropriate version number to be uploaded.

Step 2: In the terminal you will have to create the new build of the distribution. To do so run;

```bash
python3 setup.py sdist bdist_wheel
```
This will create the new distribution build file in your local repository. 

Step 3: Delete the old version of the build by navigating to the file in your local repository and deleting it 
by whatever method you prefer. 

Step 4: Add and commit the new changes and push to the remote repository.

Step 5: Merge the changes into master to update the master branch. 

Step 6: Navigate back to your terminal window and run;
```bash
git checkout master
git pull
```
This will pull in the updates that you just merged into master!

Step 7: Run the following command in the terminal to upload the distribution to PyPi. 

```bash
twine upload dist/*
```
## Summary
In summary, the only minimum requirements for using the application are;
1. Setting up a working python environment as described above. 
1. Installing the pybeecn application as described above with the following command once you have a working 
python environment;

```bash
pip install pybeecn2
```


## Further Collaboration
If you would like to contribute to the effort to improve Portland's BEECN program through the use of available data 
please contact Gabe McBride at [gabe.l.mcbride@gmail.com](mailto:gabe.l.mcbride@gmail.com).
  
## Useful links if you need additional help!
Below are a number of useful links if the instructions are not sufficient. Additionally, if you need any help you are 
welcome to contact the original developer via email above.

[GitHub Guide](https://guides.github.com/introduction/flow/), 
[Stackoverflow](https://stackoverflow.com/questions/19695127/git-workflow-review), 
[Atlassian](https://www.atlassian.com/git/tutorials/comparing-workflows), 
[Pypi](https://packaging.python.org/tutorials/packaging-projects/), and 
[ANACONDA FOR PYTHON](https://www.anaconda.com/what-is-anaconda/)

## Data Used
Data used for this project can be found at the Portland Maps Open Data website [Here](https://www.portlandoregon.gov/civic/56897). 
The data was downloaded via the APIs provided on the website for both BEECN locations and Population boundaries. 
