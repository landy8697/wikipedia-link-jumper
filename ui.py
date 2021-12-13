from tkinter import *
from tkinter import ttk, messagebox
import json
import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import sys
import webbrowser

'''
OPEN IN WEB BROWSER
NEW TK WINDOW WITH PATH
'''
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
	height=18,
	fieldbackground="#D3D3D3"
	)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
# Change selected color
style.map('Treeview', 
	background=[('selected', 'blue')])

class Node:
	def __init__(self, link, prev):
		self.link = link
		self.next = None
		self.prev = prev
		self.title = None
		self.redirects = None

global cur
cur = Node(None, None)

def get_new_links(URL, random):
	global cur
	page = requests.get(URL)
	if random:
		cur = Node(None, None)
	newNode = Node(page.url, cur)
	cur.next = newNode
	cur = newNode
	get_links(page.url)

def get_links(URL):
	global cur
	print(URL)
	page = requests.get(URL)
	page.encoding = 'ISO-885901'
	soup = BeautifulSoup(page.text, 'html.parser')

	title = soup.find("title").getText()
	print(title)
	cur.title = title
	ref = soup.find(class_="mw-headline",id="References")
	if ref is not None:
		for element in ref.find_all_next():
			element.decompose()

	links = set()
	#Code to filter out external links to wikimedia etc, file links, non english links, 
	for link in soup.findAll('a'):
		if (link.get('href') is not None and '/wiki/' == link.get('href')[0:6] and 'Wikipedia' not in link.get('href') and 'Special' not in link.get('href') and 'File' not in link.get('href') and 'Help' not in link.get('href') and link.get('class') != 'interlanguage-link interwiki-th mw-list-item' 
		and link.get('class') != 'interlanguage-link-target' and link.get('class')!='extiw'):
			links.add((link.getText(), link.get('href')))
	print("Links recovered")
	cur.redirects = links
	insert(links)

def random_article():
	get_new_links("https://en.wikipedia.org/wiki/Special:Random", True)

def select_article():
	selected = my_tree.focus()
	print(selected)
	if selected == '0' or selected == '1':
		print("Invalid")
		return
	values = my_tree.item(selected, 'values')
	
	get_new_links('https://en.wikipedia.org'+values[1], False)

def insert(data):
	for record in my_tree.get_children():
		my_tree.delete(record)
	
	my_tree.insert(parent='', index='end', iid=0, tags=('special',), values=(f"Total article links on this page", len(data)))
	my_tree.insert(parent='', index='end', iid=1, tags=('special',), values=(f"Current Article", cur.title))
	count = 2
	for record in data:
		if count % 2 == 0:
			my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]), tags=('evenrow',))
		else:
			my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1]), tags=('oddrow',))
		count+=1

def back():
	global cur
	if(cur.link is None or cur.prev.link is None):
		return
	cur = cur.prev
	insert(cur.redirects)

def forward():
	global cur
	if(cur.next.link is None):
		return
	cur = cur.next
	insert(cur.redirects)

def open_article():
	selected = my_tree.focus()
	print(selected)
	if selected == '0':
		print("Invalid")
	elif selected == '1':
		webbrowser.open(cur.link)
	else:
		values = my_tree.item(selected, 'values')
		webbrowser.open('https://en.wikipedia.org'+values[1])


button_frame = Frame(root)
button_frame.pack(pady=20)
photo = PhotoImage(file = r"left_arrow.png").subsample(10, 10)
back_button = Button(button_frame, image=photo, command=back)
back_button.grid(row=0, column=0)
random_button = Button(button_frame, text="Random article", command=random_article)
random_button.grid(row=0, column=1)
browser_button = Button(button_frame, text="Open article in browser", command=open_article)
browser_button.grid(row=0, column=2)
select_button = Button(button_frame, text="Display links", command=select_article)
select_button.grid(row=0, column=3)
photo2 = PhotoImage(file = r"right_arrow.png").subsample(10, 10)
forward_button = Button(button_frame, image=photo2, command=forward)
forward_button.grid(row=0, column=4)

tree_frame = Frame(root)
tree_frame.pack(pady=0)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended",height=17)
my_tree.pack()
tree_scroll.config(command=my_tree.yview)

my_tree['columns'] = ("Original Text", "Link")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("Original Text", anchor=W, width=300)
my_tree.column("Link", anchor=W, width=500)
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Original Text", text="Original Text", anchor=W)
my_tree.heading("Link", text="Link", anchor=W)

my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")
my_tree.tag_configure('special', background="lightgreen")

root.mainloop()
