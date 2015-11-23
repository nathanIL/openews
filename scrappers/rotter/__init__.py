import scrappers


class Rotter(scrappers.Scrapper):
    """
    Rotter forum scrapper: http://rotter.net/scoopscache.html
    From side experiment, we can do something similar to:
    gs = goslate.Goslate()
    for file in [ join('pages',f) for f in listdir('pages') if isfile(join('pages',f)) ]:
    posts = BeautifulSoup(open(file), "html.parser").find_all('font', attrs={"class": "text15bn"})
    for p in posts:
        text = p.find('b').text
        #translated = gs.translate(text, 'en')
        print(text)
        #print(translated)

    """
    pass
