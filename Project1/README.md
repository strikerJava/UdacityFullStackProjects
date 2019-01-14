# README #
This is the first submission for the 'Udacity Full Stack Web Development'. 

### How do I use this? ###
To use this python code, you need to bring this into the vagrant machine setup in the course. Download the vagrant file, then use 'vagrant up' to start it. 'vagrant ssh' to log into the machine.
Then using the newsdata.sql file provided, load it in using 'psql -d news -f newsdata.sql'. Finally, use 'python reportingtool.py' to run the program and see what the results are. 

### Design ###
Using the default table.
For the first query, the table is queried and then the top 3 articles are gotten in a 3d-array. The answers are then printed out 
For the second query, the table is queried for the authors and hits based on a substring of the slug. Slugs that dont resolve are skipped. 
For the third query, the results are seperated by the code and by the date. 
The program then iterates through in groups of two and does the percentage calculation. 
