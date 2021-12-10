from tkinter import *
from tkinter import ttk, messagebox
import json
import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import sys
import webbrowser


root = Tk()  
root.geometry('1280x720')  
root.title('Wikipedia Link Jumper')
root.iconbitmap('wiki.ico')


style = ttk.Style()
style.theme_use("default")
# Configure our treeview colors

style.configure("Treeview", 
	background="#D3D3D3",
	foreground="black",
	rowheight=25,
	height=12,
	fieldbackground="#D3D3D3"
	)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
# Change selected color
style.map('Treeview', 
	background=[('selected', 'blue')])

def get_links(URL):
	print(URL)
	page = requests.get(URL)
	page.encoding = 'ISO-885901'
	soup = BeautifulSoup(page.text, 'html.parser')

	ref = soup.find(class_="mw-headline",id="References")
	if ref is not None:
		for element in ref.find_all_next():
			element.decompose()

	links = set()
	#Code to filter out external links to wikimedia etc, file links, non english links, 
	for link in soup.findAll('a'):
		if (link.get('href') is not None and '/wiki/' in link.get('href') and 'Wikipedia' not in link.get('href') and 'Special' not in link.get('href') and 'File' not in link.get('href') and link.get('class') != 'interlanguage-link interwiki-th mw-list-item' 
		and link.get('class') != 'interlanguage-link-target' and link.get('class')!='extiw'):
			links.add((link.getText(), link.get('href')))
	print("Links recovered")
	insert(links)

def random_article():
	get_links("https://en.wikipedia.org/wiki/Special:Random")

def select_article():
	selected = my_tree.focus()
	print(selected)
	if selected == '0':
		print("First value")
		return
	values = my_tree.item(selected, 'values')
	get_links('https://en.wikipedia.org'+values[1])

def insert(data):
	for record in my_tree.get_children():
		my_tree.delete(record)
	
	my_tree.insert(parent='', index='end', iid=0, tags=('evenrow',), values=(f"Total article links on this page", len(data)))
	count = 1
	for record in data:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]), tags=('oddrow',))
		count+=1

#click_btn= PhotoImage(file='clickme.png')

button_frame = Frame(root)
button_frame.pack(pady=10)
random_button = Button(button_frame, text="Random article", command=random_article)
random_button.grid(row=0, column=0)
select_button = Button(button_frame, text="Visit selected article", command=select_article)
select_button.grid(row=0, column=1)
# Create Treeview Frame
tree_frame = Frame(root)
tree_frame.pack(pady=10)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=15)

my_tree.pack()

tree_scroll.config(command=my_tree.yview)

# Define Our Columns
my_tree['columns'] = ("Original Text", "Link")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Original Text", anchor=W, width=300)
my_tree.column("Link", anchor=W, width=600)
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Original Text", text="Original Text", anchor=W)
my_tree.heading("Link", text="Link", anchor=W)

# Create striped row tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")


root.mainloop()
