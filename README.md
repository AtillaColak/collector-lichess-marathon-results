# collector_lichess_results
Collector for lichess previous marathon tournaments.
The code I used was not optimized and was slow when iterating over 20 Marathon results.

Therefore, I wrote another version with multiprocessing. However, Lichess API doesn't allow more than 2 concurrent requests. So I set the number of worker processes to 2. 


Marathon Tournaments page: https://lichess.org/tournament/history/marathon
