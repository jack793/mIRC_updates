from bs4 import BeautifulSoup
import requests

url = "http://spacejam.ovh/New_pwd=fibra.php#top"  # target URL
new_film = []  # TOP TEN res

r = requests.get(url)

data = r.text

soup = BeautifulSoup(data, "html.parser")


def extract_film(cont: int, row: int):
    if row == 10:  # Base case: I have top ten Bluray 1080p film
        print("parsing terminato")
    else:
        for item in soup.find_all("a", class_="titolo ricerca pos" + str(row)):
            cont = cont + 1
            if cont == 4:
                new_film.append(item.string)
                extract_film(0, row + 1)  # Recursion: reset counter and increase row


extract_film(cont=0, row=0)  # Create top ten updated film inside new_film list
dump_list = new_film    # dump of new_film

# print(len(new_film))  # it's 10, it's a top ten
print(new_film)
