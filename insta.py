import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
from bs4 import BeautifulSoup
import psutil
import pandas as pd
from GoogleDriveCSVHandler import GoogleDriveCSVHandler  # Import the class

# Function to open tabs and fetch followers
def open_tabs_and_fetch_followers(profile_dict, df, csv_handler, file_name):
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9223")
    
    driver = None
    try:
        driver = webdriver.Chrome(options=options)

        for person, link in tqdm(profile_dict.items(), desc="Opening Links", unit="link"):
            driver.get(link)

            try:
                # Wait for the page to load completely
                time.sleep(random.uniform(1, 3))  # Random delay to avoid detection

                # Save the page source to a variable
                page_source = driver.page_source
                
                # Parse the page source with BeautifulSoup
                soup = BeautifulSoup(page_source, 'html.parser')
                button_class = "xat24cr"
                button = soup.find_all('span', class_=button_class)
                inner_html_list = [span.decode_contents() for span in button]

                # Ensure there are enough spans found
                if len(inner_html_list) > 1:
                    print(f"\n{person} : {inner_html_list[1]} Followers")
                    # Update the DataFrame with the follower count as a string
                    df.loc[df['Full Name'] == person, 'Number of Followers'] = str(inner_html_list[1])
                    
                    # Call the write function to update the CSV on Google Drive
                    csv_handler.update_csv(df, file_name)

                else:
                    print(f"No follower count found for {person}")

            except Exception as e:
                print(f"Error fetching data from {link}: {e}")

            # Pause between opening profiles to avoid triggering anti-scraping measures
            # time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    print("Accessing Google Drive")
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = r'C:\Users\Xcient\Desktop\scrapper\instagram leads\insta-followers-436814-5ae711b379dd.json'
    
    # File name on Google Drive
    file_name = 'final_merged_file.csv'
    
    # Initialize the GoogleDriveCSVHandler class
    csv_handler = GoogleDriveCSVHandler(SERVICE_ACCOUNT_FILE, SCOPES)
    # Call the function to read the CSV file from Google Drive
    df = csv_handler.read_csv(file_name)

    if df is not None:
        print("Got Csv")

        pre = 21000
        next = 23219
        persons = df['Full Name'].to_list()
        links = df['Profile Link'].tolist()
        followers = df['Number of Followers'].tolist()
        followers = [f for f in followers if pd.notnull(f)]
        profile_dict = dict(zip(persons[pre:next], links[pre:next]))
        
        print(f"Total {len(followers)}\nLast Processed entries\n{persons[pre]}\n{links[pre]}")
        
        # Process the profiles and update the CSV file on Google Drive
        open_tabs_and_fetch_followers(profile_dict, df, csv_handler, file_name)
    else:
        print("CSV file could not be loaded.")
# # "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223 --user-data-dir="C:/Chrome_Session"
# # # "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:/Chrome_Session"
# import time
# import random
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from tqdm import tqdm
# from bs4 import BeautifulSoup
# import pandas as pd
# from GoogleDriveCSVHandler import GoogleDriveCSVHandler  # Import the class

# def open_tabs_and_fetch_followers(profile_dict, df, csv_handler, file_name):
#     options = Options()
#     options.add_experimental_option("debuggerAddress", "localhost:9223")
    
#     driver = None
#     try:
#         driver = webdriver.Chrome(options=options)

#         for person, link in tqdm(profile_dict.items(), desc="Opening Links", unit="link"):
#             driver.get(link)

#             try:
#                 # Wait for the page to load completely
#                 time.sleep(1)
#                 # time.sleep(random.uniform(1, 3))  # Random delay to avoid detection

#                 # Save the page source to a variable
#                 page_source = driver.page_source
                
#                 # Parse the page source with BeautifulSoup
#                 soup = BeautifulSoup(page_source, 'html.parser')
#                 button_class = "xat24cr"
#                 button = soup.find_all('span', class_=button_class)
#                 inner_html_list = [span.decode_contents() for span in button]

#                 # Ensure there are enough spans found
#                 if len(inner_html_list) > 1:
#                     print(f"\n{person} : {inner_html_list[1]} Followers")
#                     # Update the DataFrame with the follower count as a string
#                     df.loc[df['Full Name'] == person, 'Number of Followers'] = str(inner_html_list[1])
                    
#                     # Call the write function to update the CSV on Google Drive
#                     followers_col_length = csv_handler.update_csv(df, file_name)
#                     print(f"Real-time followers column length: {followers_col_length}")

#                 else:
#                     print(f"No follower count found for {person}")

#             except Exception as e:
#                 print(f"Error fetching data from {link}: {e}")

#             # Pause between opening profiles to avoid triggering anti-scraping measures

#     except Exception as e:
#         print(f"Error: {e}")
    
#     finally:
#         if driver:
#             driver.quit()

# if __name__ == "__main__":
#     print("Fetching Csv")
#     SCOPES = ['https://www.googleapis.com/auth/drive']
#     SERVICE_ACCOUNT_FILE = r'C:\Users\Xcient\Desktop\scrapper\instagram leads\insta-followers-436814-5ae711b379dd.json'
    
#     # File name on Google Drive
#     file_name = 'final_merged_file.csv'
    
#     # Initialize the GoogleDriveCSVHandler class
#     csv_handler = GoogleDriveCSVHandler(SERVICE_ACCOUNT_FILE, SCOPES)
    
#     # Call the function to read the CSV file from Google Drive
#     df = csv_handler.read_csv(file_name)

#     if df is not None:
#         print("Csv Loaded")
#         pre = 23911
#         next = 25000
#         persons = df['Full Name'].to_list()
#         links = df['Profile Link'].tolist()
#         followers = df['Number of Followers'].tolist()
#         followers = [f for f in followers if pd.notnull(f)]
#         profile_dict = dict(zip(persons[pre:next], links[pre:next]))
        
#         print(f"Total {len(followers)}\nLast Processed entries\n{persons[pre]}\n{links[pre]}")
        
#         # Process the profiles and update the CSV file on Google Drive
#         open_tabs_and_fetch_followers(profile_dict, df, csv_handler, file_name)
#     else:
#         print("CSV file could not be loaded.")
