from src.CastsCommandHandler import CastsCommandHandler


def new_url_content_fetcher(file_name):
    return lambda url: open('tests/data/' + file_name, 'r').read()


def test_get_5_latest_casts():
    message_handler = CastsCommandHandler(new_url_content_fetcher('youtube-casts-five.json'))

    assert message_handler.get_response_for('!casts') == [
        "5 Latest youtube videos:",
        "Supreme Commander Forged Alliance Forever: Anaryl & Steinklotz by KBodLdIi00ezUQbTYuZnVQ - http://www.youtube.com/watch?v=kf89NSzZJwI - 2015-04-04 (0 likes)",
        "Let's (Re)play Supreme Commander Forged Alliance #20 - Purer Stress by kuenssi - http://www.youtube.com/watch?v=FHOPgEtCQuQ - 2015-04-04 (0 likes)",
        "Supreme Commander Forged Alliance Early Access Free Download by Sw2oXWDu4PaSLbFrSWhF4w - http://www.youtube.com/watch?v=5NXd8JMXWc0 - 2015-04-04 (0 likes)",
        "Countdown to Insanity! - Supreme Commander Forged Alliance by brnkoinsanity - http://www.youtube.com/watch?v=okrX1FI1iGM - 2015-04-04 (20 likes)",
        "Gyle's Patreon campaign is now live... by felixlighta - http://www.youtube.com/watch?v=SN8ujL1iMWU - 2015-04-03 (230 likes)"
    ]
