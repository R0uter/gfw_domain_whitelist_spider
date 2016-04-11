##Spider for GFW white domain list (v0.1 alpha 5)
This is a simple spider for the GFW white domain list that I wroted.

It will automatically gather domian  infomation from Chinternet and save them into database.

Finally we can generate GFW white domain list to use in pac file.

###Python
This project uses python3

##Get start

###packages
You need install python packages blow:
    
    urllib3,certifi,re,subprocess,shlex,codecs,chardet,dnspython3

If you don not have pip3,you need install pip3 first, eg.ubuntu:

    sudo apt-get install python3-pip
    
###use

Check spider function `python3 main.py status` if report like this:
    
    Spider is not running.
    
    Now we have 0 whitelist item!
    
    Top 10 here:
    
It means spider goes well, use `python3 main.py start` to start spider.

###help
    
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
To use this spider, you need MySQL Server, and a database which has table like this:

    CREATE TABLE WhiteList
    (
    DomainRank int NOT NULL,
    Domain varchar(255) NOT NULL,
    LastUpdate date NOT NULL,
    PRIMARY KEY (Domain)
    )

It can not work on Windows I think....
