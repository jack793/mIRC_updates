from bs4 import BeautifulSoup
import requests

url = "http://spacejam.ovh/New_pwd=fibra.php"  # target URL
new_film = []  # TOP TEN res

r = requests.get(url)

data = r.text

soup = BeautifulSoup(data, "html.parser")


def extract_film(cont: int, row: int, film: list) -> list:
    if row == 10:  # Base case: I have top ten Bluray 1080p film
        print("parsing terminated..returning the list ("+str(len(film))+" elements inside)")
        return film
    else:
        for item in soup.find_all("a", class_="titolo ricerca pos" + str(row)):
            cont = cont + 1
            if cont == 4:
                film.append(item.string)
                extract_film(0, row + 1, film)  # Recursion: reset counter and increase row


# dump_list = extract_film(cont=0, row=0)  # Create a dump on new_film list
# print(new_film)


