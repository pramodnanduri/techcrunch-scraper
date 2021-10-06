How to run: 
1. In the bash terminal you can run this project using: 
python server.py
2. To scrape the urls from techcrunch you can access http://localhost:8000/scrape
3. To view the urls by author you can access: http://localhost:8000/get_articles_by_author_name/Manish%20Singh

Answers to followups: 
1. What modifications would you make if we wanted to display the recent articles in as close real-time as possible? 

A. If the articles needs to be displayed in near real time, we can have an automated crawl job based on airflow or jenkins ,  
that runs every few minutes(configurable till techcrunch starts throttling us). So each crawl job can publish events to a 
kafka queue to add any parsing logics and this data can be save in our database. 

2. How would the system work/need to change if we had to collect articles from multiple sites, scaling to >10M websites (assume URLs of sites are known) on a daily basis? What kind of data design choices you will make? 
Just worry about static content (words and images).

A. If multiple sites needs to be collected, we need to configure our crawl jobs to be as reusable as possible. Since each website crawl strategy can be different,
our crawler itself can be divided into subparts like : multi threaded url downloader, page/json parser which should invoke the data into common storage layer to 
save the content into the required format of our db tables. 
Regarding the data storage, since we might get >10M urls each day, we can chose to have a NoSQL storage to store the data. 

3. Some of these websites update hourly, some monthly. We don’t know how often a website updates based on its URL. How would you design an intelligent system that minimizes unnecessary downloads/crawls? You can make reasonable assumptions based on what you know about blogs and newspaper websites.

A. We should set up configurable rules per each website domain. Initially system starts with more frequent crawls. Each time the page data changes the system should keep track 
of time the page actually changed. Based on these timings of how frequently the page changes, if the frequency of change for a website is high it should move to a high frequncy queue. 
If the frequency is low, it should be moved to a low frequency queues . We can setup different delayed queues which does the crawling at a certain interval. 
Based on how frequently the website data change the respective domain will be promoted or expelled to a low priority queue. In this way we can avoid unwanted crawls. 

4. How would you store the data in production?

A. Assuming the question is more about the way data is stored and not the actual design, All the data in production should follow proper encryption for Personal information(PII) if any. 
For non personal information data, access to the data should be restricted only to the resources that require tha actual access. If there is any file storage , each bucket permissions needs to be 
restricted only to certain access.

5. In order to curb misinformation, your CEO wants to be able to find all recent websites that mention a particular keyword like “coronavirus” or “Pfizer COVID vaccine”, how would you support her request if it’s one-off? How would you support her request if it’s a recurring ask?
    - Be very specific, answers like “put it in Snowflake” aren’t acceptable.

A. If its a one off request, I would run a batch job which filters out the data containing only above keywords. If we store the data in a Hadoop like system, we can run a map reduce job 
   to aggregate the data containing only the required keywords. Since its a one-off request this would most like be a script that scans all the data in background without effecting the performance of the system. 
   If its a recurring task, thats when I would start building a search engine. We can index all the data based on elastic search/lucene based search engine. In the elastic search we index the data and 
   also add specific index patterns to index the whole content that we have in the system. So whenever we need articles with particular keywords we can search for those articles based on the 
   search engine that we built. 
