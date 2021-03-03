# streamlit_apps



Hello, thank you for checking out my small little program.


This program will allow you to analyze your portfolio based on CSV data from 3 German banks. (ING, CONSORS, COMDIRECT)

I have included test files, so you can try it out, even when you are not customer for any of those banks.


How the app works is simple.


It all rests on a Streamlit app frame, so it can be displayed in a web browser. 

You can either host it on your local machine, or access the hosted version here:

-----------------------------------------------------------------------------

https://share.streamlit.io/maximiliansoeren/streamlit_apps/main.py

-----------------------------------------------------------------------------

If you decide to host it on your local machine, you have to navigate to the directory you have the python file (via Terminal).

Afterwards you just type: // Note: If you have renamed the file, please exchange "main" for your new filename.

" streamlit run main.py "

Once you have the program open, you can use the 3 upload windows to upload the different csv's.

IT IS IMPORTANT THAT YOU UPLOAD THEM TO THE CORRECT UPLOAD BOX.


CONSORS | ING | COMDIRECT


This is needed because the files look different and are differently encoded, and only the right upload box will be able to read each file correctly.

Once you uploaded all the files, or however many you want, you can see the basic analysis I have done on them.

You can see your best performing positions, as well as worst performing ones. Both times measured in either € or %.

You also can see the best and worst 10 positions, also measured in € and %.

Furthermore it is possible to show the top positions, in the portfolio, by € amount and by shares.

Lastly you have full access to the newly build and sorted DataFrame at the very bottom of the page.

I hope you enjoy this little project.


Best regards



Maximilian
