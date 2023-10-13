            "sharing": {
                "facebook": false,

                "google": false,


              {% if site.github_username %}
                "github": true,
                "github_link": "https://github.com/{{ site.github_username }}",
              {% else %}
                "github": false,
              {% endif %}

                "telegram": false,
                "telegram_link": "https://t.me",

                "instapaper": false,

              {% if site.twitter_username %}
                "twitter": true,
                "twitter_link": "https://twitter.com/{{ site.twitter_username }}",
              {% else %}
                "twitter": false,
              {% endif %}

                "vk": false,

                "weibo": false,

                "all": ["facebook", "twitter", "instapaper", "github", "telegram"]
            },
