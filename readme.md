# Data Coolection and Persistence

�@�~�ت�:�A�Ѹ�Ƥ��R���Ĥ@�Ӷ��q�A�p��ä[�ƫO�s���(Persistence)

�@�~�ؼ�:���Twitter����ƶi��`���A�һ`���쪺��ƪ��¤�r�ɻݤj��1G(JSON��CSV���@�榡�F��1G)
-------------------
## Data Format
-------------------
###JSON�����[�c
    {
        "user_lang": "es", 
        "user_id_str": "2566312439", 
        "user_description": "Instagram: gonzalodvillalba\nSnap: gonzalodariov", 
        "user_default_profile": false, 
        "user_profile_sidebar_border_color": "000000", 
        "user_friends_count": 191, 
        "user_utc_offset": -10800, 
        "id": 720480578160693248, 
        "user_id": 2566312439, 
        "user_profile_link_color": "3B94D9", 
        "user_profile_text_color": "333333", 
        "user_profile_use_background_image": true, 
        "user_screen_name": "gonzalodarioo", 
        "user_location": "", 
        "user_favourites_count": 905, 
        "retweet_count": 1, 
        "user_name": "Gonzalo Villalba", 
        "user_profile_image_url": "http://pbs.twimg.com/profile_images/711385903571341312/ZPltaV1S_normal.jpg", 
        "user_followers_count": 202, 
        "user_profile_background_color": "123D52", 
        "tweet_text": "@Walezequiel51 - gonza no compres ni a palo amigo!\nGonza: ya compre... https://t.co/tuAojS15Fx", 
        "user_profile_sidebar_fill_color": "DDEEF6", 
        "user_created_at": "Tue May 27 02:11:58 +0000 2014", 
        "user_profile_background_tile": true, 
        "user_listed_count": 2, 
        "url": "http://twitter.com/gonzalodarioo/status/720480578160693248/photo/1", 
        "created_at": "Thu Apr 14 05:15:30 +0000 2016", 
        "user_contributors_enabled": false, 
        "user_time_zone": "Buenos Aires", 
        "user_total_tweets": 5174
    }

###CSV��Fields

['id', 'created_at', 'tweet_text','retweet_count','user_id', 'user_name', 'user_created_at','user_location','user_screen_name','user_friends_count' , 
'user_followers_count','user_favourites_count','user_total_tweets','user_listed_count','user_profile_sidebar_fill_color','user_profile_sidebar_border_color',
'user_profile_image_url','user_description','user_lang','user_time_zone','user_profile_link_color','user_profile_background_tile','user_id_str','user_default_profile',
'user_contributors_enabled','user_utc_offset','user_profile_use_background_image','user_profile_text_color','user_profile_background_color','url']

## Data Sources
-------------------

*API�ӷ�:The Twitter Search API 
*���e�D�D:����&�B�ʬ����K��
*�U���d�ߦr��:q="fintech","mlb","nba" 