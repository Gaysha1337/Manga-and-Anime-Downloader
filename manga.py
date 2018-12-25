import requests, os
from bs4 import BeautifulSoup

print("WELCOME TO MY MANGA DOWNLOADER, THIS SCRIPT WILL DOWNLOAD ANY MANGA ")

print("\n")
print("DEAR USER, IF MY SCRIPT CANNOT FIND YOUR MANGA,")
print("PLEASE VISIT THE LINK BELOW AND ENTER IN THE NAME OF THE MANGA")
print("PLEASE COPY EVERYTHING AFTER THE LAST SLASH ('/' )")
print("AN EXAMPLE: https://manganelo.com/manga/read_tokyo_ghoul_manga_online_free4")
print("COPY THIS BIT FROM THE LINK ABOVE: read_tokyo_ghoul_manga_online_free4 AND PASTE IT")
print("\n")

print("PLEASE NOTE DEPENDING ON THE AMOUNT OF CHAPTERS IN YOUR SPECFIED MANGA, THIS PROCESS MIGHT TAKE A WHILE")
print("PLEASE NOTE THAT YOU MAY ONLY RENAME THE FOLDERS ONCE YOUR MANGA HAS BEEN DOWNLOADED, ELSE THE SCRIPT WILL CRASH")
print("\n")

manga_input = input("Type or paste a manga name ").strip().lower()
manga_root_dir = os.path.join(os.path.expanduser("~/Desktop"),"Manga")
current_manga_dir = os.path.join(manga_root_dir,manga_input.capitalize())

 # Makes a "root" for all downloaded mangas; Makes a folder that keeps all ur downloaded manga
if not os.path.isdir(manga_root_dir):
    os.mkdir(manga_root_dir)
    print("Manag root made; Current directory {}".format(manga_root_dir))
else:
    print("You already have a manga root")

if not os.path.isdir(current_manga_dir):
    os.mkdir(current_manga_dir)
    print("A folder for {} has been made in the manga root directory".format(manga_input.capitalize()))
else:
    print("You already have a folder for {}, if you would like to redownload this manga, please delete its folder".format(manga_input.capitalize()))
os.chdir(current_manga_dir)

def write_meta_data_file():
    meta_data_li_tags = soup.find("ul",attrs={"class":"manga-info-text"}).findChildren("li")
    meta_data_list = [tag.text.strip() for tag in meta_data_li_tags]
    for datum in meta_data_list:
        meta_data_list.pop(4)
        meta_data_list.pop(-1)
    meta_data_list[1] = meta_data_list[1].replace("\n","")
    with open("info.txt","w",encoding='utf-8') as f:
        f.write("\n".join(meta_data_list))
        
url = "https://manganelo.com/manga/{}".format(manga_input.replace(" ","_")) # url = "https://manganelo.com/manga/read_deadman_wonderland"
chapter_list_html = requests.get(url).content

# HTML RELATED
soup = BeautifulSoup(chapter_list_html,"html.parser")
chapter_divs = soup.find_all("div",attrs={"class":"row"})

# CHAPTER RELATED
chapter_links = [a.get("href") for div in chapter_divs for span in div.findChildren("span") for a in span.find_all("a")][::-1]
number_of_chapters = len(chapter_links)

write_meta_data_file()

img_info = []
for link in chapter_links:
    current_chapter_number = chapter_links.index(link) + 1
    current_chapter_soup = BeautifulSoup(requests.get(link).content,"html.parser")
    img_holder_div = current_chapter_soup.find("div",attrs={"id":"vungdoc"})
    img_links = [link.get("src") for link in img_holder_div.find_all("img")]
    print("------------------------- Chapter Link Appended: {} ----------------------------".format(current_chapter_number))
    chapter_info = {"chapter_number":current_chapter_number,"img_links":img_links}
    img_info.append(chapter_info)

for img_dict in img_info:
    img_chapter = img_dict.get("chapter_number")
    current_chapter_dir = os.path.join(current_manga_dir,str(img_chapter))
    for link in img_dict.get("img_links"):
        current_page_number = img_dict.get("img_links").index(link) + 1
        
        if not os.path.isdir(current_chapter_dir):
            os.mkdir(current_chapter_dir)
        os.chdir(current_chapter_dir)

        img_request = requests.get(link)
        filename = manga_input.capitalize() + " " + str(current_page_number) + ".jpg"

        with open(filename, "wb") as f:
            f.write(img_request.content)
    print("------------- Dowloaded Chapter {}; there are {} pages in this chapter ----------".format(img_chapter,len(img_dict.get("img_links"))))

print("All chapters downloaded")




        
        
        
        
    

            


