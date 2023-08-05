import os

def femaSetProxies():
    os.environ["HTTP_PROXY"] = 'http://proxy.apps.dhs.gov:80'
    os.environ["HTTPS_PROXY"] = 'http://proxy.apps.dhs.gov:80'