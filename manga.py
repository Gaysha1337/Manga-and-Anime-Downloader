import requests, os
from bs4 import BeautifulSoup
from terminaltables import AsciiTable

query = input("Type a manga title (can be a keyword): ")

query_url = "https://manganelo.com/search/{}".format(query.strip().replace(" ","_"))
request_query_html = requests.get(query_url).content

soup = BeautifulSoup(request_query_html,"html.parser")

query_div_items = soup.find("div",attrs={"class":"daily-update"}).findChildren("a")
query_info_dicts = [{"q_link":a.get("href"),"q_name":a.text} for a in query_div_items if not a.has_attr("class")]
manga_links = [i.find("a").get("href") for i in soup.select(".story_name")]
manga_choices = [i.find("a").text for i in soup.select(".story_name")]


def create_manga_choice_table(manga_choices):
    data = []
    choice_number = 0
    for choice in manga_choices:
        choice_number += 1
        data.append(['Manga Name: ' + choice, 'Manga Number: ' + str(choice_number)])
    table = AsciiTable(data)
    table.inner_heading_row_border = False
    table.title = "Manga Choices: "
    print(table.table)
    return int(input("\nDear User, please type in the number that corresponds to the manga that you wish to download: ").strip())

user_number_choice = create_manga_choice_table(manga_choices)
print(manga_links[user_number_choice - 1]) # prints the url of the user's chosen manga name
manga_input = manga_choices[user_number_choice - 1]

manga_root_dir = os.path.join(os.path.expanduser("~/Desktop"),"Manga")
current_manga_dir = os.path.join(manga_root_dir,manga_input)

 # Makes a "root" for all downloaded mangas; Makes a folder that keeps all ur downloaded manga
if not os.path.isdir(manga_root_dir):
    os.mkdir(manga_root_dir)
    print("Manga root made; Current directory {}".format(manga_root_dir))
else:
    print("You already have a manga root")

if not os.path.isdir(current_manga_dir):
    os.mkdir(current_manga_dir)
    print("A folder for {} has been made in the manga root directory".format(manga_input.capitalize()))
else:
    print("You already have a folder for {}, if you would like to redownload this manga, please delete its folder".format(manga_input.capitalize()))
os.chdir(current_manga_dir)

url = manga_links[user_number_choice - 1]

def write_meta_data_file():
    meta_data_li_tags = soup.find("ul",attrs={"class":"manga-info-text"}).findChildren("li")
    summary_div = soup.find("div",attrs={"id":"noidungm"})
    split_summary = summary_div.text.strip().split()[1::]
    formatted_summary = "\n"    
    for word in split_summary:
        if "." in word or "," in word or word == split_summary[1]:
            word+="\n"
        formatted_summary += word + " "
    meta_data_list = [tag.text.strip() for tag in meta_data_li_tags]
    for datum in meta_data_list:
        meta_data_list.pop(4)
        meta_data_list.pop(-1)
    meta_data_list[1] = meta_data_list[1].replace("\n","")
    with open("info.txt","w",encoding='utf-8') as f:
        f.write("\n".join(meta_data_list))
        f.write(formatted_summary)

chapter_list_html = requests.get(url).content

# HTML RELATED
soup = BeautifulSoup(chapter_list_html,"html.parser")
chapter_divs = soup.find_all("div",attrs={"class":"row"})

# CHAPTER RELATED
chapter_links = [a.get("href") for div in chapter_divs for span in div.findChildren("span") for a in span.find_all("a")][::-1]
chapter_names = iter([a.get("title") for div in chapter_divs for span in div.findChildren("span") for a in span.find_all("a")][::-1])
number_of_chapters = len(chapter_links)

write_meta_data_file()

img_info = []
for link in chapter_links:
    current_chapter_number = chapter_links.index(link) + 1
    current_chapter_soup = BeautifulSoup(requests.get(link).content,"html.parser")
    img_holder_div = current_chapter_soup.find("div",attrs={"id":"vungdoc"})
    img_links = [link.get("src") for link in img_holder_div.find_all("img")]
    print("------------------------- Chapter Link Appended: {} ----------------------------".format(current_chapter_number))
    chapter_info = {"chapter_number":current_chapter_number,"chapter_name":next(chapter_names),"img_links":img_links}
    img_info.append(chapter_info)
    
for img_dict in img_info:
    img_chapter = img_dict.get("chapter_number")
    chapter_name = img_dict.get("chapter_name")
    current_chapter_dir = os.path.join(current_manga_dir,str(chapter_name).replace(":"," - "))

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

