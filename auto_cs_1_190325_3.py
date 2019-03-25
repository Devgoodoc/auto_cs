import tkinter as tk
from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter import messagebox as msg
import datetime
#from slackclient import SlackClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from threading import Thread
import json
import requests
#=====================================
win = tk.Tk()

win.title("CS 등록 프로그램")

win.resizable(False, False)

frame1 = tk.LabelFrame(win, text=' 기본정보 입력')
frame1.grid(row=0, column=0, padx=5, pady=5)

frame2 = tk.LabelFrame(win, text=' 5. 문의내용')
frame2.grid(row=1, column=0, padx=5, pady=5)

frame7 = tk.LabelFrame(win, text=' 6. 처리내용')
frame7.grid(row=2, column=0, padx=5, pady=5)

frame3 = tk.LabelFrame(win, text=' 7. CS 채널 선택')
frame3.grid(row=3, column=0, padx=5, pady=5)

frame4 = tk.LabelFrame(win, text=' 8. 처리 담당자 지정 (※ 슬랙 알림 발송)')
frame4.grid(row=4, column=0, padx=5, pady=5)

frame5 = tk.LabelFrame(win, text=' 9. 처리 상태 ')
frame5.grid(row=5, column=0, padx=5, pady=5)

frame6 = tk.LabelFrame(win, text='10. CS 등록하기')
frame6.grid(row=6, column=0, padx=5, pady=5)

#-------------------------------------
# 전역변수1
search_result = ""      # 트리뷰 정보가 담긴 변수
add_win_1 = ""          # 외부 윈도우 창 정보가 담긴 변수

# 구글스프레드 시트 인증 정보
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)

# Key 정보 인증
gs = gspread.authorize(credentials)

# CS접수현황 문서 가져오기
doc = gs.open_by_url('https://docs.google.com/spreadsheets/d/15N7K31hkeaqb8Snq7D2U2N6jTjvtLQ5pip4iW1DK4TU/edit?pli=1#gid=0')
ws = doc.get_worksheet(0)  # 첫번째 시트 선택

# 병원 접수 도입현황 문서 가져오기
doc_2 = gs.open_by_url('https://docs.google.com/spreadsheets/d/1iRpmebKnV31cfS9xStu8GedjOxKPmObSAnnZaX-M65A/edit?pli=1#gid=1759562169')
ws_2 = doc_2.get_worksheet(0)

# 지정 열 데이터를 리스트 형태로 가져오기
val_1 = ws_2.col_values('2')                # 병원명
val_2 = ws_2.col_values('23')               # 연동차트
val_3 = ws_2.col_values('24')               # 설치버전
val_4 = ws_2.col_values('19')               # 설치 시 특이사항
val_5 = ws_2.col_values('16')               # 요양기관번호
val_6 = ws_2.col_values('13')               # 전화번호
val_7 = ws_2.col_values('17')               # 주소

#print(val_1)

#ws_2.update_acell('S2131', '-')

#=====================================
# 병원 검색 버튼 이벤트
def _opensearch():
	global search_result
	global add_win_1

	if not hospital_name_box.get():
		msg.showwarning("경고", "병원명을 입력해주세요!")
		return

	print("입력한 병원명입니다! : ", hospital_name_box.get())
	print('---')

	# 입력받은 병원명 검색

	result_index = []
	result_list = []

	#print(len(val_1))
	#print(range(len(val_1)))
	#print(val_1[1691])
	#print(val_1[1813])
	print(val_7[849].strip())


	for n in range(len(val_1)):
		if hospital_name_box.get() in val_1[n]:
			# 문자열이 포함된 병원명을 배열에 추가
			#print(val_1[n])
			#print(val_5[n])
			#print(val_7[n])
			#print("이건 인덱스넘버: ", val_1.index(val_1[n]))
			#print(val_7[val_1.index(val_1[n])])

			if not val_5[n]:
				continue
			else:
				result_list.append(val_5[n])

	for n4 in range(len(result_list)):
		# 요양기관번호 기준으로 인덱스 값 추출하여 배열에 넣는다.
		result_index.append(val_5.index(result_list[n4]))

	print(result_list)
	print(result_index)

	if not result_index:
		msg.showwarning("경고", "검색결과가 없습니다!")
		return

#	print(result_list)
	#print(result_index)

	# 검색 결과 창 그리기
	add_win_1 = Toplevel(win)
	add_win_1.title("검색 결과")
	add_win_1.geometry("1150x470")
	add_win_1.resizable(False, False)

	# 트리 뷰 그리기
	#columns_number = ['#0', '#1', '#2', '#3', '#4', '#5', '#6', '#7']
	columns_list = ['hospital_name', 'chart_name', 'install_version', 'install_uniqueness', 'hospital_code', 'hospital_phone_number', 'hospital_address']
	columns_name = ['병원명', '사용차트', '버전', '설치 시 특이사항', '요양기관번호', '전화번호', '주소']

	search_result = tk.ttk.Treeview(add_win_1, columns=columns_list, height=20, padding=20)

	search_result.column('#0', width=30)                    # No
	search_result.heading('#0', text='*')

	search_result.column('#1', width=170)                   # 병원명
	search_result.heading('#1', text=columns_name[0])

	search_result.column('#2', width=80)                   # 사용차트
	search_result.heading('#2', text=columns_name[1])

	search_result.column('#3', width=30)                    # 설치버전
	search_result.heading('#3', text=columns_name[2])

	search_result.column('#4', width=150)                   # 설치 시 특이사항
	search_result.heading('#4', text=columns_name[3])

	search_result.column('#5', width=100)                   # 요양기관번호
	search_result.heading('#5', text=columns_name[4])

	search_result.column('#6', width=100)                   # 전화번호
	search_result.heading('#6', text=columns_name[5])

	search_result.column('#7', width=400)                   # 주소
	search_result.heading('#7', text=columns_name[6])

	# 데이터 삽입 처리 2
	for n2 in range(len(result_index)):
		n3 = result_index[n2]
		search_result.insert('', 'end', text="*", value=[val_1[n3], val_2[n3], val_3[n3], val_4[n3], val_5[n3], val_6[n3], val_7[n3].strip()])

	search_result.bind('<Double-Button-1>', selectData)     # 더블클릭 이벤트 바인딩 

	search_result.pack()                                    # 최종 화면 그리기

def selectData(event):                                      # 검색 데이터 더블클릭 시 발생하는 이벤트
	#print(event)
	get_data_1 = search_result.identify_row(event.y)
	#print("get_data_1: ", get_data_1)
	get_data_2 = search_result.set(get_data_1)              # 선택한 json 데이터 정보 가져오기
	print("get_data_2: ",get_data_2)

	search_data_0 = get_data_2['hospital_name']
	search_data_1 = get_data_2['chart_name']
	search_data_2 = get_data_2['install_version']
	search_data_3 = get_data_2['hospital_code']
	search_data_4 = get_data_2['hospital_phone_number']
	search_data_5 = get_data_2['install_uniqueness']

	# 조회 값 초기화
	hospital_name_box.delete(0, END)
	ocschart_name_box.set('')                         # 연동 차트
	version_string_box.delete(0, END)                 # 사용 버전
	unique_hospital_number_box.delete(0, END)         # 요양기관번호
	hospital_phone_number_box.delete(0, END)          # 병원 전화번호
	install_uniqueness_box.delete(0, END)             # 설치 시 특이사항

	# 조회 값 입력
	hospital_name_box.insert(INSERT, search_data_0)
	ocschart_name_box.insert(INSERT, search_data_1)
	version_string_box.insert(INSERT, search_data_2)
	unique_hospital_number_box.insert(INSERT, search_data_3)
	hospital_phone_number_box.insert(INSERT, search_data_4)
	install_uniqueness_box.insert(INSERT, search_data_5)

	ask_type_1_choose.focus()

	add_win_1.destroy()                               # 검색 결과 창 닫기

def click_me():                                       # 검색 버튼 클릭 시 command에 담아야 할 이벤트
	create_thread()                                   # 쓰레드 메서드 호출
	print("create thread : search")
	print('---')

def create_thread():
	run_thread = Thread(target=_opensearch)           # 메서드 대상 지정
	run_thread.setDaemon(True)
	run_thread.start()
	print('검색 쓰레드 시작 : ', run_thread)
	print('---')

def click_me_2():                                     # 등록 버튼 클릭 시 command에 담아야 할 이벤트
	create_thread()
	print("create thread : press")
	print('---')

def create_thread_2():
	run_thread = Thread(target=_enrollment)           # 메서드 대상 지정
	run_thread.setDaemon(True)
	run_thread.start()
	print(run_thread)
	print('---')

def press_enter(event):                               # 엔터 키 입력 시, 검색 수행
	click_me()
	print("키 입력이 들어왔다 : i am enter")
	print('---')

#def press_korean_key():
	#win.bind('<>', )
	#win32api.LoadKeyboardLayout('00000412', 1)
	#print('hi korea')
#py_win_keyboard_layout.load_keyboard_layout("00000412")

#=====================================
#=====================================
# 전역/날짜 변수
now = str(datetime.datetime.now())
today = str(datetime.date.today())

# 영문 요일
day_of_week = str(datetime.date.today().strftime("%A"))

day_of_week_2 = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

hero_codes = ['<@U3B3XCG74>', '<@U891L2SUS>', '<@UDVCMQN5A>', '<@U5UTV83DW>', '<@U93KUCV27>', '<@UDRQ9JHN2>', '<@UGM6EAYHW>', '<@UGXR0EN5D>']

slack_url_0 = 'https://hooks.slack.com/services/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'  # cs_오류처리
slack_url_1 = 'https://hooks.slack.com/services/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'  # cs_설치이슈
slack_url_2 = 'https://hooks.slack.com/services/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'  # cs_장비이슈
slack_url_3 = 'https://hooks.slack.com/services/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'  # cs_철수요청
slack_url_4 = 'https://hooks.slack.com/services/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'  # cs_알림톡등록_병원명
slack_url_5 = 'https://hooks.slack.com/services/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'  # cs_기타문의

slack_channel_list = [slack_url_0, slack_url_1, slack_url_2, slack_url_3, slack_url_4, slack_url_5]

value_1 = list()        # 처리담당자 값을 담는 배열

value_2 = list()        # 처리담당자 값을 담아 한글이름값을 담는 배열

codes_1 = list()        # hero_code 값을 담는 배열

#=====================================
# 등록하기 버튼 이벤트
def _enrollment():
	# 토큰 리프레쉬
	if credentials.access_token_expired:
		gs.login()
		msg.showwarning("경고", "토큰이 만료되어 재로그인을 수행했습니다. \n '뀨우!' 버튼을 다시 눌러주세요.")
		return

	# 오류 처리 알림
	if not goodocmon_choose.get():
		msg.showwarning('경고', 'CS 접수자를 선택해주세요.')
		return
	if not hospital_name_box.get():
		msg.showwarning('경고', '병원명을 입력해주세요.')
		return
	if not ocschart_name_box.get():
		msg.showwarning('경고', '연동차트를 선택해주세요.')
		return
	if not ask_type_1_choose.get():
		msg.showwarning('경고', '문의 유형을 선택해주세요.')
		return
	if not ask_type_2_choose.get():
		msg.showwarning('경고', '문의 유형을 선택해주세요.')
		return
	if not ask_contents.get('1.0', END).strip():
		msg.showwarning('경고', '문의내용을 입력해주세요.')
		return
	if not cs_state.get():
		msg.showwarning('경고', '처리 상태를 선택해주세요.')
		return

	# CS 처리 상태 값 전환
	if cs_state.get() == 1:
		cs_result = state_list[0]
	elif cs_state.get() == 2:
		cs_result = state_list[1]
	elif cs_state.get() == 3:
		cs_result = state_list[2]

	# 날짜 정보 수집
	getDayNumber = datetime.date(int(receipt_date_box.get()[0:4]),int(receipt_date_box.get()[5:7]),int(receipt_date_box.get()[8:10])).weekday()

	# 날짜 변환
	if getDayNumber == 0:
		day_of_korean = day_of_week_2[0]
	elif getDayNumber == 1:
		day_of_korean = day_of_week_2[1]
	elif getDayNumber == 2:
		day_of_korean = day_of_week_2[2]
	elif getDayNumber == 3:
		day_of_korean = day_of_week_2[3]
	elif getDayNumber == 4:
		day_of_korean = day_of_week_2[4]
	elif getDayNumber == 5:
		day_of_korean = day_of_week_2[5]
	elif getDayNumber == 6:
		day_of_korean = day_of_week_2[6]

	# 처리 담당자 선택 값 수집
	for n in range(len(hero_list)):
		value_1.append(hero_states[n].get())    # 체크박스의 상태값을 배열에 추가한다.

		if value_1[n] == 1:
			codes_1.append(hero_codes[n])       # 체크된 이름의 hero_code를 배열에 추가한다.
			value_2.append(hero_list[n])        # 체크된 상태값의 한글이름을 담는 배열

	# 스프레드 시트 행 데이터 셋팅
	cs_data_list = [receipt_date_box.get(), day_of_korean, hospital_name_box.get(), unique_hospital_number_box.get(), hospital_phone_number_box.get(),
	                ask_contents.get('1.0', END).strip(), goodocmon_choose.get(), ocschart_name_box.get(), ask_type_1_choose.get(),
	                ask_type_2_choose.get(), cs_result, "", success_contents.get('1.0',END).strip(), ",\n".join(value_2)]

	# 리스트 형태의 데이터를 행 단위로 데이터를 체크해서 자동으로 비어있는 다음행에 넣어줌
	ws.append_row(cs_data_list)

	# 채널 선택 값 수집
	final_channel = channel_state.get()

	if final_channel == 0:
		channel_name = slack_channel_list[0]
	elif final_channel == 1:
		channel_name = slack_channel_list[1]
	elif final_channel == 2:
		channel_name = slack_channel_list[2]
	elif final_channel == 3:
		channel_name = slack_channel_list[3]
	elif final_channel == 4:
		channel_name = slack_channel_list[4]
	elif final_channel == 5:
		channel_name = slack_channel_list[5]

	# 슬랙 메세지 셋팅
	message_1 = "■ 병원명: " + hospital_name_box.get() + '\n' + \
	            "■ 연동차트명: " +  ocschart_name_box.get() + '\n' + \
	            "■ 요양기관번호: " + unique_hospital_number_box.get() + '\n' + \
	            "■ 사용버전: " + version_string_box.get() + '\n' + \
				"■ 전화번호: " + hospital_phone_number_box.get() + '\n' + \
				"■ 문의유형: " + ask_type_2_choose.get() + '\n' + \
				"■ CS 접수자: " + goodocmon_choose.get() + '\n' + \
				'\n' + \
				"▣ 문의내용" + '\n' +  ask_contents.get('1.0', END).strip() + '\n' + \
				'\n' + \
	            "▣ 처리 담당자" + '\n' + ",".join(codes_1) + '\n' + \
	            '\n' + \
	            "▣ 처리 내용" + '\n' + success_contents.get('1.0', END).strip() + '\n' + \
	            '\n' + \
	            "▣ 처리상태" + '\n' + cs_result

	content = message_1
	payload = {"text": content}

	# 배포용 슬랙 메세지
	request_result = requests.post(channel_name, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
	#print(request_result)
	if request_result.status_code != 200:
		msg.showwarning('앗! 이런..', '슬랙 메시지 전송에 실패했습니다.' )
		return

	# 테스트용 슬랙 메세지
	#test_slack_channel_url = 'https://hooks.slack.com/services/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'
	#test_request_result = requests.post(test_slack_channel_url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})
	#print(test_request_result.status_code)
	#if test_request_result.status_code != 200:
	#	msg.showwarning('앗! 이런..', '슬랙 메시지 전송에 실패했습니다.' )
	#	return

	msg.showinfo('결과', 'CS 등록이 완료되었습니다.')		# 등록완료 메세지 호출

	# 입력값 초기화
	hospital_name_box.delete(0, END)                        # 병원명 초기화
	ocschart_name_box.set('')                               # 연동차트 초기화
	ask_type_1_choose.set('')                               # 문의유형(대) 초기화
	ask_type_2_choose.set('')                               # 문의유형(중) 초기화
	ask_contents.delete('1.0', END)                         # 접수내용 초기화
	success_contents.delete('1.0', END)                     # 처리내용 초기화

	ocschart_name_box.set('')                               # 연동 차트
	version_string_box.delete(0, END)                       # 사용 버전
	unique_hospital_number_box.delete(0, END)               # 요양기관번호
	hospital_phone_number_box.delete(0, END)                # 병원 전화번호
	install_uniqueness_box.delete(0, END)                   # 설치 시 특이사항

	value_1.clear()                                         # 처리담당자 값을 담는 배열 초기화
	codes_1.clear()                                         # hero_code 값을 담는 배열 초기화

	hospital_name_box.focus()                               # 병원명 입력 칸으로 포커싱 이동

#=====================================
# 접수 일자
ttk.Label(frame1, text='* 접수 일자').grid(row=0, column=0, padx=0, pady=0, sticky='W')

# 접수 일자 입력 박스
receipt_date = tk.StringVar()                               # 기입창에 표시할 문자열을 가져올 변수
receipt_date_box = ttk.Entry(frame1, width=20, textvariable=receipt_date)
receipt_date_box.grid(row=0, column=1, padx=5, pady=5, columnspan=2, sticky='W')

receipt_date_box.insert(INSERT, today)

#-------------------------------------
# 접수자
ttk.Label(frame1, text='1. CS 접수자').grid(row=0, column=3,  padx=0, pady=0, sticky='W')

# 접수자 입력 박스
goodocmon = tk.StringVar()
goodocmon_choose = ttk.Combobox(frame1, width=20, textvariable=goodocmon, state='readonly')
goodocmon_choose['values'] = ('데이브', '스미스', '테오', '도로시', '르윈', '벨라', '폴', '스테파니')
goodocmon_choose.grid(row=0, column=4, padx=5, pady=5, columnspan=1)
goodocmon_choose.current()

#-------------------------------------
# 병원명
ttk.Label(frame1, text='2. 병원명 입력').grid(row=1, column=0, padx=0, pady=0, sticky='W')

# 병원명 입력 박스
hospital_name = tk.StringVar()
hospital_name_box = ttk.Entry(frame1, width=14, textvariable=hospital_name)
hospital_name_box.grid(row=1, column=1, padx=5, pady=5, columnspan=2, sticky='W')

#-------------------------------------
# 병원 검색 버튼
search_button = tk.Button(frame1, width=4, text='검색!', command=click_me)
search_button.grid(row=1, column=1, padx=5, pady=5, columnspan=3)
search_button.bind('<Return>', press_enter)

#-------------------------------------
# 연동차트
ttk.Label(frame1, text=' * 연동 차트').grid(row=1, column=3, padx=0, pady=0, sticky='W')

# 연동차트 입력 박스
ocschart_name = tk.StringVar()
ocschart_name_box = ttk.Combobox(frame1, width=20, textvariable=ocschart_name)
ocschart_name_box['values'] \
	= ('의사랑', '오케이차트', '이지스', '비연동', '스마트CRM', '아이프로', '아이차트', '한의사랑', '히포크라테스', '팬차트', '해당없음')
ocschart_name_box.grid(row=1, column=4, padx=5, pady=5, columnspan=1)
ocschart_name_box.current()

# 사용 버전
ttk.Label(frame1, text=' - 사용 버전').grid(row=2, column=0, padx=0, pady=0, sticky='W')

# 사용 버전 표시 박스
version_string = tk.StringVar()
version_string_box = ttk.Entry(frame1, width=20, textvariable=version_string, state='normal', takefocus=False)
version_string_box.grid(row=2, column=1, padx=5, pady=5, columnspan=2, sticky='W')

# 요양기관번호
ttk.Label(frame1, text=' - 요양기관번호').grid(row=2, column=3, padx=0, pady=0, sticky='W')

# 요양기관번호 표시 박스
unique_hospital_number = tk.StringVar()
unique_hospital_number_box = ttk.Entry(frame1, width=22, textvariable=unique_hospital_number, state='normal', takefocus=False)
unique_hospital_number_box.grid(row=2, column=4, padx=5, pady=5, columnspan=2, sticky='W')

# 전화번호
ttk.Label(frame1, text=' - 전화번호').grid(row=3, column=0, padx=0, pady=0, sticky='W')

# 전화번호 표시 박스
hospital_phone_number = tk.StringVar()
hospital_phone_number_box = ttk.Entry(frame1, width=20, textvariable=hospital_phone_number, state='normal', takefocus=False)
hospital_phone_number_box.grid(row=3, column=1, padx=5, pady=5, columnspan=2, sticky='W')

# 특이사항
ttk.Label(frame1, text=' - 설치 시 특이사항').grid(row=3, column=3, padx=0, pady=0, sticky='W')

# 특이사항 표시 박스
install_uniqueness = tk.StringVar()
install_uniqueness_box = ttk.Entry(frame1, width=22, textvariable=install_uniqueness, state='normal', takefocus=False)
install_uniqueness_box.grid(row=3, column=4, padx=5, pady=5, columnspan=2, sticky='W')

#-------------------------------------
#-------------------------------------
# 문의유형(대)
ttk.Label(frame1, text='3. 문의 유형(대)').grid(row=4, column=0, padx=0, pady=0, sticky='W')

# 문의유형(대) 입력 박스
ask_type_1 = tk.StringVar()
ask_type_1_choose = ttk.Combobox(frame1, width=18, textvariable=ask_type_1, state='readonly')
ask_type_1_choose['values'] = ('사용중', '신청/기타', '설치시')
ask_type_1_choose.grid(row=4, column=1, padx=5, pady=5, columnspan=2, sticky='W')
ask_type_1_choose.current()

#-------------------------------------
# 문의유형(중)
ttk.Label(frame1, text='4. 문의 유형(중)').grid(row=4, column=3, padx=0, pady=0, sticky='W')

# 문의유형(중) 입력 박스
ask_type_2 = tk.StringVar()
ask_type_2_choose = ttk.Combobox(frame1, width=20, textvariable=ask_type_2, state='readonly')
ask_type_2_choose['values'] = \
	('접수프로그램사용 이슈', '거치대/충전 이슈', '태블릿 이슈', '알림톡 이슈', '차트 연동 이슈', 'USB통신 이슈',
	 '[요청] 기능개선요청', '[요청] 프로그램 추가설치', '백신프로그램 이슈', '개인정보 이슈',
	 '사용 미숙', '네트워크 불안정', '의사랑 보안 이슈', 'PC환경이슈',
	 '업그레이드 이슈', '철수', '복합', '기타')
ask_type_2_choose.grid(row=4, column=4, padx=5, pady=5, columnspan=1)
ask_type_2_choose.current()

#-------------------------------------
# 문의 내용
#ttk.Label(win, text='* 문의 내용').grid(row=1, column=0, padx=0, pady=0, sticky='W')

# 문의 내용 입력 박스
scroll_w1 = 67
scroll_h1 = 10
ask_contents = scrolledtext.ScrolledText(frame2, width=scroll_w1, height=scroll_h1, wrap=tk.CHAR)      # => wrap option=CHAR/WORD
ask_contents.grid(row=0, column=0, columnspan=3, padx=5, pady=1, sticky='W')

#-------------------------------------
# 처리내용

# 처리 내용 입력 박스
scroll_w1 = 67
scroll_h1 = 10
success_contents = scrolledtext.ScrolledText(frame7, width=scroll_w1, height=scroll_h1, wrap=tk.CHAR)      # => wrap option=CHAR/WORD
success_contents.grid(row=0, column=0, columnspan=3, padx=5, pady=1, sticky='W')

#-------------------------------------
# CS 채널 선택 라디오 버튼
cs_channel_combo_row = 0
cs_channel_combo_row_2 = 1

channel_state = tk.IntVar()

channel_list = ['오류처리', '설치이슈', '장비이슈', '철수/반품요청', '알림톡 등록', '기타문의' ]

for col2 in range(6):
	channel_radio = tk.Radiobutton(frame3, text=channel_list[col2], variable=channel_state, value=col2)
	channel_radio.grid(row=cs_channel_combo_row, column=col2)
'''
cs_channel_1 = tk.IntVar()
cs_channel_1 = tk.Checkbutton(frame4, text="오류처리", variable=cs_channel_1)
cs_channel_1.grid(row=hero_combo_row, column=0, sticky='W')
cs_channel_1.deselect()
'''

#-------------------------------------
# 처리 담당자 지정
#ttk.Label(frame2, text='* 처리 담당자 지정 (※ 슬랙 알림 발송)').grid(row=1, column=0, padx=0, pady=0, sticky='W')

# 처리 담당자 선택 콤보 박스
hero_combo_row = 0
hero_combo_row_2 = 1

def _clickCombo():
	value_1.append()

hero_list = ['데이브', '스미스', '테오', '도로시', '르윈', '벨라', '폴', '스테파니']

#hero_state = tk.IntVar()
hero_state_0 = tk.IntVar()
hero_state_1 = tk.IntVar()
hero_state_2 = tk.IntVar()
hero_state_3 = tk.IntVar()
hero_state_4 = tk.IntVar()
hero_state_5 = tk.IntVar()
hero_state_6 = tk.IntVar()
hero_state_7 = tk.IntVar()

hero_states = [hero_state_0, hero_state_1, hero_state_2, hero_state_3, hero_state_4, hero_state_5, hero_state_6, hero_state_7]

for col in range(len(hero_states)):
	#hero_state[col] = tk.IntVar()
	hero_name_box = tk.Checkbutton(frame4, text=hero_list[col], variable=hero_states[col])
	hero_name_box.grid(row=hero_combo_row, column=col)
'''
hero_state_0 = tk.IntVar()     # 체크버튼의 상태를 저장할 제어 변수
hero_name_0 = tk.Checkbutton(frame3, text=hero_list[0], variable=hero_state_0)
hero_name_0.grid(row=hero_combo_row, column=0, sticky='W')
hero_name_0.deselect()
'''

#-------------------------------------
# 처리 상태
#ttk.Label(frame3, text='* 처리 상태').grid(row=0, column=0, padx=0, pady=0, sticky='W')

# 처리 상태 선택 라디오 박스
cs_state_combo_row = 0

#def _clickCombo_2():
	#return cs_state.get()

state_list = ['처리중', '처리완료', '보류']

cs_state = tk.IntVar()

cs_radio_1 = tk.Radiobutton(frame5, text=state_list[0], variable=cs_state, value=1)
cs_radio_1.grid(row=cs_state_combo_row, column=0)
cs_radio_1.deselect()

cs_radio_2 = tk.Radiobutton(frame5, text=state_list[1], variable=cs_state, value=2)
cs_radio_2.grid(row=cs_state_combo_row, column=1)
cs_radio_2.deselect()

cs_radio_3 = tk.Radiobutton(frame5, text=state_list[2], variable=cs_state, value=3)
cs_radio_3.grid(row=cs_state_combo_row, column=2)
cs_radio_3.deselect()

#-------------------------------------
# CS 등록하기
#ttk.Label(win, text='* CS 등록하기').grid(row=10, column=0, sticky='W')

# CS 등록하기 버튼
action_1 = ttk.Button(frame6, text="뀨우!", command=create_thread_2).grid(row=0, column=0, padx=5, pady=5)

#=====================================
# 최초 실행 시 포커싱 위치 = CS 접수자
goodocmon_choose.focus()
#=====================================
win.mainloop()