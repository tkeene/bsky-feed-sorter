# Released under MIT license by kobolds-keep.net
# Please let me know what you do with it!

my_account = ''
my_password = '' # Recommend using an app password to bypass

print("Starting client, this may take a few seconds...")

from atproto import Client, client_utils
import time

def main():
    client = Client()
    #import pprint
    #pprint.pprint(dir(client))

    profile = client.login(my_account, my_password)
    print('welcome,', profile.display_name)

    # https://atproto.blue/en/latest/readme.html
    # text = client_utils.TextBuilder().text('hello world from ').link('python sdk', 'https://atproto.blue')
    # post = client.send_post(text)
    # client.like(post.uri, post.cid)

    #my_profile = client.get_profile(my_account)
    users = []

    print("...making another query...")
    query = client.get_follows(my_account)
    OLDEST_DATE = "2000-01-01"
    NUMBER_TO_INDEX = 2000
    while query.cursor and len(users) < NUMBER_TO_INDEX:
        for f in query.follows:
            if len(users) < NUMBER_TO_INDEX:
                #time.sleep(0.1)
                remaining_tries = 5
                while remaining_tries > 0:
                    try:
                        print(len(users), ": Indexing ", f.handle)
                        data = {}
                        data["handle"] = f.handle
                        response = client.get_author_feed(actor=f.handle)
                        feed = response.feed
                        newest_date = OLDEST_DATE
                        for i in range(0, min(5, len(feed))):
                            next_date = feed[i].post.indexed_at
                            if next_date > newest_date:
                                #print(next_date, "is newer than", newest_date)
                                newest_date = next_date
                        data["date"] = newest_date
                        if "2023" in newest_date or "2000" in newest_date:
                            print("2023!!!")
                        elif "2024" in newest_date:
                            print("Just a 2024...")
                        elif "2025" not in newest_date[0:4]:
                            print(newest_date[0:4])
                        users.append(data)
                        remaining_tries = 0
                    except:
                        print("ERROR1")
                        time.sleep(2)
                        remaining_tries = remaining_tries - 1
        try:
            query = client.get_follows(my_account, query.cursor)
        except:
            print("ERROR2")
            break
        time.sleep(1)

    print("Indexed", len(users), "entries")
    print("Sorting...")
    users = sorted(users, key=lambda user: user["date"])
    print("Output")
    for i in range(50):
        user =users[i]
        print(user["handle"], user["date"])

if __name__ == '__main__':
    main()
