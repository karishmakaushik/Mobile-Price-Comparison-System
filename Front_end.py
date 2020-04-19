#Library Used

import tkinter as tk
import Back_end
from tkinter import messagebox
import webbrowser

#checking for the main file 

if __name__ == '__main__':
    
    # creating main window
    root = tk.Tk()
    
    # getting original screen data
    X = root.winfo_screenwidth()
    Y = root.winfo_screenheight()

    # normal window size
    x = 1280
    y = 720
    
    # title
    root.title('Mobile Price Compare')
    
    # root icon
    root.iconbitmap('mobile.ico')
    
    # setting root geometr
    root.geometry(str(x) + 'x' + str(y) + '+120+30')
    
    
    root.minsize(640, 680)
    root.maxsize(X, Y)

    # color = 'honeydew3'
    color = 'gray92'

    root.configure(bg=color)
    
    # It is used as container for other widget
    frame = tk.Frame(root)
    frame.pack(fill='both')

    frame.configure(bg=color)

    # function for the management of the space between widget
    def space(n=1):
        for i in range(n):
            # It is widget to display the text on the window
            tk.Label(frame, text=' ', background=color).pack()


    space(3)
    
    # It is widget to display the text on the window
    tk.Label(frame, text='Enter Mobile Name', font=('Comic Sans MS', 25, 'bold'), \
             foreground='firebrick3', background=color).pack()

    space()
    
    # tkinter special Variable (String)
    entry = tk.StringVar()
    #  It is a widget to display a single-line text field for accepting values from a user.
    tk.Entry(frame, font=("verdana", 11), textvariable=entry, bd=3, relief='ridge', \
             background='azure').pack(ipadx=120, ipady=4)

    space()

    flag = 1


    def get_price():
        
        # for maintaing local bound error
        global flag

        if flag == 1:
            # function for getting input from the user and parsing into the back-end code
            Back_end.generate_link(entry.get())
            
            data = Back_end.fetch_and_parse()

            if not data:
                # This widget is to display the any message to the user
                messagebox.showinfo('Mobile not found',
                                    'The mobile phone you are looking for is not available, try another search')
            else:
                flag = 0
                try:
                    # function for the scraping of the data
                    result = Back_end.scrap(data)

                    info = []

                    for key in result:
                        l = []
                        # the scraped data is in the form of dictionary converting it into the list of list for the display purpose
                        for value in result[key]:
                            l.append(value)
                        info.append(l)

                    Back_end.create_dictionary()

                    space(1)
                    
                    # for displaying lines and text
                    C = tk.Canvas(frame, background=color, highlightthickness=0)
                    C.pack()

                    for i in range(len(info[0])):
                        tk.Label(C, text=info[0][i], font=("calibari", 10), foreground='black', \
                                 bd=1, padx=50, background=color).grid(row=i, column=0)
                        tk.Label(C, text=info[2][i], font=("calibari", 10, 'bold'), foreground='black', \
                                 bd=2, relief='groove', background='ivory').grid(row=i, column=1)
                    else:
                        global last_row
                        last_row = i
                    
                    # function for canvas space
                    def canvas_space(n=1):
                        global last_row
                        for i in range(n):
                            last_row += 1
                            tk.Label(C, text='', background=color).grid(row=last_row)
                    
                    # tkinter variable (Integer)
                    store_choice = tk.IntVar()
                    
                    # maining spaces in the canvas
                    canvas_space(1)

                    def sel():
                        global selection
                        selection = store_choice.get()

                    def go_to_store():
                        webbrowser.open_new_tab(info[3][selection])

                    tk.Label(C, text='Buy-Now', background=color, font=('Comic Sans MS', 15, 'bold')).grid(
                        row=last_row + 1)

                    canvas_space(1)

                    for i in range(len(info[0])):
                        last_row += 1
                        #  widget is used to display a number of options as radio buttons.
                        #  The user can select only one option at a time.
                        tk.Radiobutton(C, text=info[0][i], variable=store_choice, value=i, \
                                       command=sel, background=color, activeforeground='blue', pady=2).grid(
                            row=last_row)

                    canvas_space(1)
                    # display buttons in your application
                    tk.Button(C, text="Go to Store", command=go_to_store, relief='ridge', \
                              padx=20, background='thistle', activebackground='lime green').grid(row=last_row + 1,
                                                                                                 column=1)
                    # function to create a new canvas and distroy the last one
                    def new():
                        global flag
                        C.destroy()
                        flag = 1
                        frame.update()

                    canvas_space(2)
                    tk.Button(C, text="Try another Search", command=new, relief='ridge', \
                              padx=20, background='light salmon', activebackground='red').grid(row=last_row + 3,
                
                # handling error                                                                                column=1)
                except IndexError:
                    messagebox.showerror('Something Wrong', 'Currently this mobile phone data is not visible to you')
                    flag = 1

        else:
                                                                                               
            messagebox.showinfo('Search box is not Empty', 'Press "Try another search" and try again')


    tk.Button(frame, text="Search", command=get_price, background='azure', borderwidth=1, \
              padx=30, activebackground='Springgreen2', relief='ridge').pack()
    # main event loop to take action against each event triggered by the user and repeatedly displaying the window                                                                                          
    root.mainloop()