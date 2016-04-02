#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import Spider
import IO






def main():
    io = IO.IO()
    spider = Spider.Spider(io)
    spider.start()

    pass





if __name__=='__main__':
    main()