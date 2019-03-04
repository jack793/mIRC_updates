from bs4 import BeautifulSoup
import requests

url = "http://spacejam.ovh/New_pwd=fibra.php#top"  # target URL
match = ["1080p", 'AC3']  # Bluray word sometimes isn't present inside the string
new_film = []  # TOP TEN res
dump_list = []  # dump of result

r = requests.get(url)

data = r.text

soup = BeautifulSoup(data, "html.parser")

res = []


# count = 0
# for item in soup.find_all("a", class_="titolo ricerca pos" + str(idx)):
#     count = count + 1
#     if count == 4:
#         res.append(item.string)
#         break

def extract_film(cont: int, row: int):
    if row == 10:   # Base case: I have top ten Bluray 1080p film
        print("parsing terminato")
    else:
        for item in soup.find_all("a", class_="titolo ricerca pos" + str(row)):
            cont = cont + 1
            if cont == 4:
                res.append(item.string)
                extract_film(0, row + 1)  # Recursion: reset counter and increase row


extract_film(cont=0, row=0)

print(len(res))
print(res)

# count = 0
# for idx in range(0, 10):
#     for item in soup.find_all("a", class_="titolo ricerca pos" + str(idx)):
#         count = count + 1
#         if count == 4:
#             res.append(item.string)
#             count = 0

# print(res)

# while len(new_film) < 10:
#     for f_idx in range(len(res)):
#         # print(res[3+21*f_idx])
#         new_film.append(res[3+21*f_idx])
#
# print(new_film)

# for item in soup.find_all("a"):
#     if all(x in item.get_text() for x in match):  # Search for all the words in match array are found
#         res.append(item.get_text())
#
# new_film = res[:11]
# print(len(new_film))  # length of list
# print(new_film)  # Print the list of all Blu-ray 1080p AC3 latest film!
