##Spider for GFW white domain list
This is a simple spider for the GFW white domain list that I wroted.

It will automatically gather domian accessable infomation from Internet and save them into database.

Finally we can generate GFW white domain list to use in pac file.

###Python
This project uses python3

##Get start
You need install python packages blow:
    
    urllib3,certifi,re,subprocess,shlex,codecs,chardet

If you don not have pip3,you need install pip3 first, eg.ubuntu:

    sudo apt-get install python3-pip
    
Then use command like this:
    
    main.py [start|stop|restart|status|list|help]

    ------------------
    
    start    start spider
    stop     stop spider
    restart  restart spider
    status   check list status
    list     get whitelist top 10000
    help     show this page
    
###MySQL
To use this spider, you need a SQL Server, and a database which has table like this:

    CREATE TABLE WhiteList
    (
    DomainRank int NOT NULL,
    Domain varchar(255) NOT NULL,
    LastUpdate date NOT NULL,
    PRIMARY KEY (Domain)
    )

It can not work on Windows I think....
---
And ... now I'm working on...