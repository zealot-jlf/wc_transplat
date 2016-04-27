__author__ = 'linfengji'
import requests
import sys
import redis
import config

if __name__ == "__main__":
    redis_con = redis.StrictRedis(host=config.REDIS_URL, port=config.REDIS_PORT, db=config.REDIS_DB)
    url = config.ACCESS_TOKEN_URL %(config.APP_ID, config.SECRET_ID)
    response = requests.get(url)
    result = response.json()
    if result.has_key('access_token'):
        redis_con.set("wc_access_token", result['access_token'])

    url = config.SERVER_IP_URL % (result['access_token'])
    response = requests.get(url)
    result = response.json()
    with redis_con.pipeline() as pipe:
        while 1:
            try:
                pipe.watch('wc_ips')
                pipe.multi()
                pipe.delete('wc_ips')
                for ip in result['ip_list']:
                    if len(ip) > 0:
                         pipe.sadd('wc_ips', ip)
                pipe.execute()
                break
            except redis.WatchError:
                continue
            except:
                raise
            finally:
                pipe.reset()
    print "update_access_token_success"
