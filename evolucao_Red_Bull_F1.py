from bs4 import BeautifulSoup
import requests, re

site = "https://www.formula1.com"

comp_1 = re.compile(r'^/en/results.*/team/.*')
comp_2 = re.compile(r'.*rbr|.*[rR]ed.*[bB]ull.*')

rbr_results = {"results": []}


for year in range(2005,2023):

    url = f"https://www.formula1.com/en/results.html/{year}/team.html"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')
    
    all_links = [a['href'] for a in soup('a') if a.has_attr('href')]
    good_links = list(set([i for i in all_links if re.match(comp_1, i)]))
    team_link = [r for r in good_links if re.match(comp_2, r)][0]

    year_html = requests.get(site+team_link).text
    soup_races = BeautifulSoup(year_html, 'html5lib')
    
    points = [float(i.text) for i in soup_races.find_all('td', {"class":"dark bold"})[1::2]]
    races = [i.text for i in soup_races.find_all('a', {'class':'dark ArchiveLink'})]

    position = [i.text for i in soup.find_all('td', {"class":"dark"})]
    filtro = list(filter(lambda x: x == str(int(sum(points))), position))
    position = [position[position.index(x)-1] for x in filtro] or "error"

    rbr_results['results'].append({
        "year":year, 
        "position": position[0] ,
        "total_points":sum(points),
        "races": [{
            "circuit": i,
            "points":points[races.index(i)]
            } for i in races]
        })

    
for r in rbr_results['results']:
    print("\n",r,"\n")

