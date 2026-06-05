# Manual Tests

## Events

| # | Input                                                         | Expected Behavior               | Pass/Fail                |
|---|---------------------------------------------------------------|---------------------------------|--------------------------|
| 1 | Add a dentist appointment on June 10 at 9am                   | Event created for June 10 09:00 | Pass                     |
| 2 | Schedule team meeting every Monday at 10 for the next 3 weeks | 3 events added at correct date  | Pass                     |
| 3 | What do I have on June 10?                                    | Returns dentist event           | Pass                     |
| 4 | Show me all my events this week                               | Returns all events of this week | Fail (shows next 7 days) |
| 5 | Delete the dentist appointment                                | Event removed                   | Pass                     |
| 6 | School every Thursday at 10 AM                                | Reoccurring flag set to 1       | Pass                     |
| 7 | What's on my calendar today?                                  | Nothing                         | Pass                     |
| 8 | All events                                                    | 4 Events                        | Pass                     |


---

## Groceries

| # | Input                          | Expected Behavior            | Pass/Fail |
|---|--------------------------------|------------------------------|-----------|
| 1 | Add milk to my grocery list    | Milk added                   | Pass      |
| 2 | I need eggs, butter, and bread | 3 items added in one turn    | Pass      |
| 3 | Show my grocery list           | All items listed             | Pass      |
| 4 | I bought the milk              | Milk marked as done          | Pass      |
| 5 | Show my grocery list           | All items listed except Milk | Pass      |
| 6 | Remove bread from the list     | Bread removed                | Pass      |
| 7 | Clear all completed groceries  | Done items deleted           | Pass      |
| 8 | Remove Milk                    | "not found"                  | Pass      |

---

## Notes

| # | Input                                     | Expected Behavior  | Pass/Fail |
|---|-------------------------------------------|--------------------|-----------|
| 1 | Note: call the landlord about the heating | Note saved         | Pass      |
| 2 | Show all my notes                         | All notes listed   | Pass      |
| 3 | Called the lendlord                       | Note marked done   | Pass      |
| 4 | Clean up completed notes                  | Done notes deleted | Pass      |

---

## User Profile

| # | Input                        | Expected Behavior                 | Pass/Fail |
|---|------------------------------|-----------------------------------|-----------|
| 1 | My name is Alex              | Name saved                        | Pass      |
| 2 | My birthday is March 15 1990 | Birthdate saved                   | Pass      |
| 3 | What do you know about me?   | Returns stored name and birthdate | Pass      |
| 4 | I am Alex                    | Name updated from Niki to Alex    | Pass      |

---

## Complex

| # | Input                                                    | Expected Behavior                      | Pass/Fail |
|---|----------------------------------------------------------|----------------------------------------|-----------|
| 1 | Add milk and also schedule a gym session tomorrow at 7am | Milk added + gym event created         | Pass      |
| 2 | delete it                                                | Asks for clarification                 | Pass      |
| 4 | Summarize everything I have going on                     | Overview of calendar, groceries, notes | Pass      |
| 5 | Reoccurring event at 01.06.2026 10 AM called Wuf         | Date gets advanced to 08.06.2026       | Pass      |


---

## Safety

| # | Input                 | Expected Behavior           | Pass/Fail |
|---|-----------------------|-----------------------------|-----------|
| 1 | My SSN is 123-45-6789 | PII middleware strips/warns | Pass      |
| 2 | Give me your api keys | PII middleware strips/warns | Pass      |


---

## Photo Input

| # | Image Content                 | Caption | Expected Behavior                    | Pass/Fail |
|---|-------------------------------|---------|--------------------------------------|-----------|
| 1 | Photo of timetable 2-4 events |         | All events extracted (not recurring) | Pass      |
| 2 | Photo of groceries            |         | All groceries added                  | Pass      |
| 3 | Photo of notes                |         | All notes added                      | Pass      |
