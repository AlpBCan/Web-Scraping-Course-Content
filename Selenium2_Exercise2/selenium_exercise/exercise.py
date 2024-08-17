'''
    It's your turn!!!

    You will use Selenium and scrape following data into an Excel file:
        author name
        author birth date
        author birth place

    Follow the instructions, try to do this by yourself. But if you are stuck,
    do not hesitate to take a look at that part of the solution and come back.

    url = https://quotes.toscrape.com/  -->  not the JS version!

'''

# Import necessary libraries, you can add some others when you need them later on.



# Create a dictionary to save the data



# Create an empty list to save the links of author pages



# Define the options, create the driver, get to the main page



# Login (the same with earlier)



# Create a loop to visit every page (this is the same with what we did earlier).
# In this loop find every author's link(from (about) section) and save them to the empy list you created.



# Take the author url list and put it in a set to remove duplicates



# Create another loop with this list and visit every page to get the name, birth date and birth place to the dictionary



# Create Pandas dataframe, put dictionary in and convert it to an Excel file
