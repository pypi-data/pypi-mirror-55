# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.


DateTime module provides us with the means to extract the date values from unstructured format. This Date-parsing library provides us the means to extract date/time values between different dates, in a more user-defined format. 

#'Last 3 days', 'Last month', '1st week of January' ,'2nd week of June to 3rd week of March'


Usage:

from dateparserlib import dates
picked_dates= dates.DateData("query")### query= sales figure between 21st Janury and 22nd December
formatted_dates= picked_dates.compile_dates()
formatted_dates
