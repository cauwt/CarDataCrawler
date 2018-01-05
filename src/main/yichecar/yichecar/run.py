# -*- coding: utf-8 -*-


def main():
    from scrapy import cmdline
    name = 'yichecar'
    cmd = 'scrapy crawl {0}'.format(name)
    cmdline.execute(cmd.split())

if __name__ == "__main__":
    main()
