import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox as msg
import datetime
from slackclient import SlackClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re

from threading import Thread

from queue import Queue
#===
# 구글스프레드 시트 인증
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)

gs = gspread.authorize(credentials)     # Key 정보 인증

# CS접수현황 문서 가져오기
doc = gs.open_by_url('https://docs.google.com/spreadsheets/d/15N7K31hkeaqb8Snq7D2U2N6jTjvtLQ5pip4iW1DK4TU/edit?pli=1#gid=0')
ws = doc.get_worksheet(0)       # 첫번째 시트 선택

# 병원 접수 도입현황 문서 가져오기
doc_2 = gs.open_by_url('https://docs.google.com/spreadsheets/d/1iRpmebKnV31cfS9xStu8GedjOxKPmObSAnnZaX-M65A/edit?pli=1#gid=1759562169')
ws_2 = doc_2.get_worksheet(0)

globals1 = '글로벌'

info3 = list()
info4 = " "
#===
class OOP():
	def __init__(self):
		self.win = tk.Tk()

		self.win.title("검색 테스트 모듈")

		self.create_widgets()

	def create_widgets(self):
		# 병원명
		ttk.Label(self.win, text='* 병원명 입력').grid(row=0, column=0, padx=0, pady=0, sticky='W')

		# 병원명 입력 박스
		self.hospital_name = tk.StringVar()
		self.hospital_name_box = ttk.Entry(self.win, width=20, textvariable=self.hospital_name)
		self.hospital_name_box.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky='W')

		# 병원 검색 버튼
		self.search_button = tk.Button(self.win, width=4, text='검색!', command=self.click_me)
		self.search_button.grid(row=0, column=4, padx=5, pady=5, columnspan=3)
		#search_button.bind('<ButtonRelease-1>')

		self.hospital_name_box.focus()

#==================================================================================================
	def _opensearch(self):
		print(self.hospital_name_box.get())

		# 데이터 찾기
		criteria_re = re.compile(self.hospital_name_box.get())
		print(criteria_re)

		cell_1 = ws_2.findall(criteria_re)                              # 입력받은 병원명을 시트에서 찾는다
		# cell_1 = ws_2.findall(hospital_name_box.get())              # 입력받은 병원명을 시트에서 찾는다
		print(cell_1)

		if not cell_1:
			msg.showwarning("경고", "검색결과가 없습니다!")
			return

		# 검색 결과 프레임 그리기
		self.add_win_1 = tk.Toplevel(self.win)
		self.add_win_1.title("검색 결과")
		self.add_win_1.geometry("800x400")
		self.add_win_1.resizable(False, False)

		# 검색 결과 트리뷰 그리기
		columns_number = ['#0', '#1', '#2', '#3', '#4', '#5']
		columns_list = ['hospital_name', 'chart_name', 'hopital_code', 'hospital_phone_number', 'hospital_address']
		columns_name = ['병원명', '사용차트', '요양기관번호', '전화번호', '주소']

		self.search_result = ttk.Treeview(self.add_win_1, columns=columns_list)
		#search_result.pack()

		self.search_result.column('#0', width=30)
		self.search_result.heading('#0', text='No')

		self.search_result.column('#1', width=150)
		self.search_result.heading('#1', text=columns_name[0])

		self.search_result.column('#2', width=100)
		self.search_result.heading('#2', text=columns_name[1])

		self.search_result.column('#3', width=100)
		self.search_result.heading('#3', text=columns_name[2])

		self.search_result.column('#4', width=100)
		self.search_result.heading('#4', text=columns_name[3])

		self.search_result.column('#5', width=300)
		self.search_result.heading('#5', text=columns_name[4])


		# 트리뷰에 데이터 삽입
		for n1 in range(len(cell_1)):
			cell_2 = cell_1[n1].row
			cell_3 = ws_2.row_values(cell_2)
			self.search_result.insert('', 'end', text=n1, iid=str(n1), value=[cell_3[1], cell_3[22], cell_3[15], cell_3[12], cell_3[16]])

		# 삽입된 데이터의 튜플 가져오기
		info = self.search_result.get_children()
		print(info)

		# 삽입된 데이터 행 단위로 추출
		#for n2 in info:
		#	info2 = search_result.set(n2)
		#	info3.append(info2)
		#	print('3', info3)

		# 삽입된 데이터 클릭 시 이벤트 바인딩
		self.search_result.bind('<Double-Button-1>', self.selectData)

		self.search_result.pack()

		msg.showinfo('알림', '검색이 완료되었습니다!')

#---
	def selectData(self, event):
		print(self, event)

		get_data_1 = self.search_result.identify_row(event.y)
		print(get_data_1)
		get_data_2 = self.search_result.set(get_data_1)
		print(get_data_2)

#---
	def click_me(self):       # 버튼 클릭 시 command에 담아야 할 이벤트
		print("hello")
		self.create_thread()  # 쓰레드 메서드 호출
		#self.use_queues()

	def create_thread(self):
		#self.run_thread = Thread(target=self.method_in_a_thread, args=[3])    # 메서드 대상 지정
		self.run_thread = Thread(target=self._opensearch)                     # 메서드 대상 지정
		self.run_thread.setDaemon(True)
		self.run_thread.start()
		print(self.run_thread)

		#write_thread = Thread(target=self.use_queues, daemon=True)
		#write_thread.start()


	'''
	def method_in_a_thread(self, num_of_loops=10):
		print("world")
		for idx in range(num_of_loops):
			print(self.hospital_name_box.get())

		print('create_thread():', self.run_thread.isAlive())
	

	def use_queues(self):
		gui_queue = Queue()     # 큐 인스턴스 생성
		print(gui_queue)

		for idx in range(10):
			gui_queue.put('큐 전용 메세지 : ' + str(idx))
		#gui_queue.put('큐 전용 메세지')
		print(gui_queue.get())

		while True:
			print(gui_queue.get())
	'''
#===

#===
start = OOP()
start.win.mainloop()