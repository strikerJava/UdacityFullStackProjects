# README #
This is the first submission for the 'Udacity Full Stack Web Development'. 

## How do I use this?
To use this python code, you need to bring this into the vagrant machine setup in the course.
* Download the vagrant file, then use `vagrant up` to start it 
* Use `vagrant ssh` to log into the machine
* Using the newsdata.sql file provided, load it in using `psql -d news -f newsdata.sql`
* Finally, use ` python reportingtool.py ` to run the program and see what the results are 

### Design 
The SQL queries are all hitting the normal table with no additional views or changes. 

* For the first query, the table is queried for both titles and count of the path where the slug from the articles table is a substring of the title from the articles table.  We only retrieve the top 3 articles , place them into a 3d-array, and then print them out. 
* For the second query, the table is queried for the authors and hits based on a substring of the slug and where the author number lines up between articles and authors.  the slugs from the articles table that don't resolve or don't exist are skipped. We then print out the results.
* For the third query, we select the count of status, the substring of the status that corresponds to the HTTP code, and the date. We then group by status and the date, and then place the results table into a 2D array.  The program then iterates through in groups of two and does the percentage calculation, printing out the ones it finds to have the matching crieria of 100% of more.  
