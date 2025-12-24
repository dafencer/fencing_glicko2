# Score-based Glicko-2 Rating Model for Fencing 
Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 



## Data Sources
This project uses data from the five legs of the 2025 PFA National Rankings for Women’s Epee (Senior category).
- [PFA 1st Leg Senior Women's Épée Ranking](https://www.fencingtimelive.com/events/results/BC6BB9DF4F3C4698ABC67C7C981EA492)
- [PFA 2nd Leg Senior Women's Épée Ranking](https://www.fencingtimelive.com/events/results/E04B7C8376F44EB9802B73BE4BF12F4E)
- [PFA 3rd Leg Senior Women's Épée Ranking](https://www.fencingtimelive.com/events/results/7F980738E0144C8DAA418ECB7FBE3124)
- [PFA 4th Leg Senior Women's Épée Ranking](https://www.fencingtimelive.com/events/results/CE92CC2A35D341FB8FF98A33F8674355)
- [PFA 5th Leg Senior Women's Épée Ranking](https://www.fencingtimelive.com/events/results/2434850A79B148CC9608A0935CB5274E)

### Data Collection
- Pool Bouts: Scraped automatically for all tournament legs using Python and Selenium from [FencingTimeLive](https://www.fencingtimelive.com/)

  The script navigates to the Pools tab, opens the Details of each pool in a separate tab, and extracts the bout order table.
  <img width="1247" height="622" alt="image" src="https://github.com/user-attachments/assets/9854d6b7-ed87-4ab4-a3de-dc4e0bbb6c2c" />


- Direct Elimination (DE) Bouts: Extracted manually by copying the full [tableau](https://www.fencingtimelive.com/tableaus/scores/BC6BB9DF4F3C4698ABC67C7C981EA492/BE91553421E241518AD27ECF74D93995) pages into a spreadsheet and processing them to retrieve individual match data.
  
### Data Cleaning
Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 

## Model Building
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Results and evaluation
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Future work

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Acknowledgments/References
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
