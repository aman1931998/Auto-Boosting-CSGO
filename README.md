# Auto-Boosting-CSGO
Fully Automated CS:GO Prime MM Boosting

This Auto Boosting panel was declared moot post Valve's update to Kill CS:GO Auto Boosting for Non-Prime to Prime accounts. Hence, I have decided to post the entire code on to github.

Features: 
1. Can handle upto 1000 accounts in a week. (Minimum 300 accounts)
2. Each account's data is stored and handled by the script. The following data is captured for each account: 
  a) Account Info: Account Owner, Username, Password, SteamID, Steam64ID, Steam Profile Link, Friend Code, Email Domain, Email Login Page, Email Address, Email Password, Target PR Rank, Trade URL
  b) Cooldown Info: Cooldown History including Cooldown Type, Time and MatchID, Last Cooldown Type, Last Cooldown Timestamp, Last Cooldown MatchID.
  c) Error Info: Total Error Count, Error History including Error Name and Time, Last Error Name, Last Error Timestamp. 
  d) Match History: Match Count, MatchIDs data including MatchID, Timestamp and Match Output.
  e) MM Rank Info: MM Rank, MM Wins, MM Rank Snippet, MM Rank History including MM Rank, Snippet, MatchID and Timestamp.
  f) Search Info: Total Search Count, Total Mismatch Count, Search History including searchID, Mismatch Count and Match Found.
  g) PR Rank Info: PR Rank, PR Rank Snippet, Current Week Number, Current Week Number Match Count, XP Gained, Weekly History including Week Index, Timestamp and XP Gained for respective week.
3. For each MM Search, data is collected in real-time by the script. The following data is captured for each MM Search Session: 
  a) SearchID
  b) Team1 and Team2
  c) Total Search Time
  d) Match Found?
  e) Search Mismatch History including the lobby receiving match and timestamp recorded.
4. For each MM Match Played, data is collected in real-time by the script. The following data is captured for each MM Match Played: 
  a) Session's IP Address
  b) MatchID
  c) SearchID
  d) Match Played On
  e) TimeStamp
  f) Match Output
  g) Team1 and Team2 Lobby Leaders
  h) Team1 and Team2 Players including their MM and PR Rank (before and after match), Week Number, Week Number Match Count, XP Gained in the match for each account.
  i) Match Time Details including Match Start Time, Match End Time, Match Duration. 
  j) Match Search Details including Search Start Time, Search End Time, Search Duration, Search Error Count.

* These above details are captured for extraction, analysis and reporting for useful information from the collected data.

5. When the automated script is initialized, the script loads all account info into the memory and creates batches of 10 accounts. Each batch can further be divided into 2 sets of 5 accounts each with same MM Rank level.

6. The first batch of 10 accounts is selected. Each Steam account is logged in, in a separate Avast Sandbox Environment and CS:GO game is launched.

7. The 10 CS:GO panels are launched of window size 640 X 480 at 10 different locations of 4K screen.

8. Each CS:GO panel opens, it is being ready up and some pre-requisites are checked. If a panel fails to launch, the script will kill the earlier PID of the panel and will relaunch it.

9. Once all panels are launched, the lobbies are created using the respective FRIEND-CODE for each account. In case the database does not have the friend code for the account, the script will fetch it up from the panel itself.

10. After Lobbies are created, some necessary checks are done, to make sure there are no issues with network connection, ports and CS:GO Panels' visual capturing.

11. The MM Search is started, at which the script checks again if there are any ping issues and handles it accordingly.

12. During the MM Search, the script regularly monitors the panels for any known issues faced during the search. If there is a MM Mismatch, the script will stop the MM Search and wait for a total of one minute before restarting the search.

13. When a MM Match is found, the Auto Accept kicks in and accepts the match. 

14. From this point onwards, the script monitors each panel till the end of the match for all necessary Match progression, Error reporting and handling as well as Monitoring activities.

15. Once the MM Match Starts, the script will disconnect each lobby once to get the Tactical Timeout out of the picture. Now, the script will disconnect the loosing lobby multiple times, keeping in mind the edge limits of the Competitive Cooldown (CD) and ends the match.

16. Once the MM Match is ended, the lobby immediately disconnects the players and captures the new MM and PR Ranks of each panel and updates the database. 

17. Based on the configuration: 
  a) A new lobby can be generated from the same batch of accounts, or 
  b) A new batch of 10 accounts can be loaded.

18. The Entire script is 100% automated and reports can be generated using running a separate reporting script.

19. The following configuration settings are available for the script.
  a) Repeat Automated?
  b) Consider Unranked Accounts?
  c) Unranked Accounts Threshold
  d) Consider Ranked Accounts?
  e) Ranked Accounts Threshold
  f) MM Batches Creation Mode ('Greedy', 'Hierarchical', 'No Rank Greedy')
  g) Shuffle Batches?
  h) Consider Cooldown for Batch Creation?
  i) Un-equality Breaker ('Match Count' or 'MM Rank')
  j) Target XP 
  k) After Launch Timeout
  l) Launch Timeout
  m) Trusted Mode
  n) Map Name
  o) Match Output ('tie' or 'winlose')
  p) Winner Score (suppressed if Match Output is 'tie')
  q) Cleanup After Each Match?
  h) Power Supply Check (for Laptops)
  i) Technical Timeout Handle?
  k) Map Time Settings: 
    i)    After DC Wait Time.
    ii)   After RC Wait Time.
    iii)  Max Time for Loading.


Skills Used in script: Python, Computer Vision, OS Integration, Mouse and KB Wrapping, Data Analysis and Reporting, Data Structures, PKL Database storage. 

Libraries used in python: tqdm, pandas, xml, os, pickle, numpy, cv2, sys, datetime, PIL, shutil, psutil, pyautogui, keyboard, pyperclip, beepy, subprocess, itertools, multiprocessing, random, argparse, time, secrets, copy.




