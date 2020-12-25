import urllib.request
import requests
from bs4 import BeautifulSoup
import sys
import os


def downloadImage(output_directory, category, resolution, start_page, end_page):
    opener = urllib.request.URLopener()
    opener.addheader("User-Agent", "whatever")

    try:
        for i in range(start_page, end_page + 1):
            if category is not None:
                soup = BeautifulSoup(
                    requests.get(
                        f"https://hdqwalls.com/category/{category}/page/{i}"
                    ).text,
                    features="html.parser",
                )
            else:
                soup = BeautifulSoup(
                    requests.get(
                        f"https://hdqwalls.com/latest-wallpapers/page/{i}"
                    ).text,
                    features="html.parser",
                )

            for wall_resp in soup.find_all("div", class_="wall-resp"):
                web_parser = BeautifulSoup(
                    requests.get(
                        "https://hdqwalls.com/"
                        + f"wallpaper/{resolution}"
                        + "-".join(wall_resp.a["href"].split("-")[:-1])
                    ).text,
                    features="html.parser",
                )
                img_url = web_parser.find("span", {"id": "c_download_btn"}).span.a[
                    "href"
                ]
                opener.retrieve(
                    img_url, f"./{output_directory}/{wall_resp.a['href'][1:]}.jpg",
                )
                print(f"Downloaded {wall_resp.a['href'][1:]}")
    except:
        print(
            "Some error occurred. Please check the url, resolution, category, start and end page"
        )


def help():
    print(
        """
Command Line tool for downloading Image from https://hdqwalls.com

-c  |  Category (-c celebrities-wallpapers)
-o  |  Output Directory (-o ./walls)
-r  |  Resolution (-r 1920x1080)
-s  |  Start Page (-s 10)
-e  |  End Page (-e 60)
-h  |  Help (-h)

Note Start Page cannot be greater than End Page
"""
    )


def error():
    print(
        """
The entered arguments are incorrect please run the file with --help or -h argument
"""
    )


def handleDirectory(directory):
    if not os.path.isdir(directory):
        os.mkdir(directory)


def main():
    commands = sys.argv[1:]
    category = None
    output_directory = "./hdqwalls/"
    resolution = "1920x1080"
    start_page = 1
    end_page = 1
    asked_help = False

    for idx, arg in enumerate(commands):
        if arg == "-c":
            category = commands[idx + 1]
        elif arg == "-o":
            output_directory = commands[idx + 1]
        elif arg == "-r":
            resolution = commands[idx + 1]
        elif arg == "-s":
            start_page = int(commands[idx + 1])
        elif arg == "-e":
            end_page = int(commands[idx + 1])
        elif arg == "-h":
            asked_help = True

    handleDirectory(output_directory)

    if start_page > end_page:
        print("Start page cannot be greater than end page")
        return

    if len(commands) == 1:
        if commands[0] == "-h":
            help()
        else:
            downloadImage(
                output_directory=output_directory,
                category=category,
                resolution=resolution,
                start_page=start_page,
                end_page=end_page,
            )
    elif asked_help and len(commands) > 1:
        error()
    else:
        downloadImage(
            output_directory=output_directory,
            category=category,
            resolution=resolution,
            start_page=start_page,
            end_page=end_page,
        )


if __name__ == "__main__":
    main()
