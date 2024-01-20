# atm-take-home

This is the simple ATM controller described in coderbyte. As stated we are only dealing with 1 dollar bills but I made the code so that it could simulate putting in multiple 1 dollar bills. If we expanded on this project and verified the number of 1 dollar bills I would pass in the information from there.

I tried to format the code so that we could expand on it once we knew what our bank API was. I also chose to repeatedly call the "bank api" in case data was updated in between our actions. Maybe its possible someone is waiting on a transfer an they already signed in. However, there are a lot more complicated cases for deadlock and concurrency issues so this is really simplified.

To clone the project:
git clone git@github.com:johankiilavirta/atm-take-home.git

github url: https://github.com/johankiilavirta/atm-take-home

To run the test cases you can just run tests.py. I did not want to use a testing framework to keep things simple. You can modify the values in the tests to verify that the tests are receiving the right values.