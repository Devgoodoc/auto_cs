import tkinter as tk
from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter import messagebox as msg
import datetime
from slackclient import SlackClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
#=====================================
# 구글스프레드 시트 인증
scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)

gs = gspread.authorize(credentials)     # Key 정보 인증

doc = gs.open_by_url('https://docs.google.com/spreadsheets/d/15N7K31hkeaqb8Snq7D2U2N6jTjvtLQ5pip4iW1DK4TU/edit?pli=1#gid=0')        # 문서 가져오기
ws = doc.get_worksheet(0)       # 첫번째 시트 선택

#val = ws.acell('B1').value      # 지정 셀 데이터 가져오기
#print(val)

#val = ws.row_values('1')        # 지정 행 데이터를 리스트 형태로 가져오기
#print(val)

#val = ws.col_values('1')        # 지정 열 데이터를 리스트 형태로 가져오기
#print(val)

#vals = ws.range('A2:B3')        # 지정 범위 데이터 데이터를 가져오기
#for val in vals:
#	print(val.value)

#ws.update_acell('A4533', 'test')    # 지정 셀에 데이터 입력

#ws.append_row(['test1','test2'])    # 리스트 형태의 데이터를 행 단위로 넣어줌. 데이터를 체크해서 자동으로 비어있는 다음행에 넣어줌

#=====================================
win = tk.Tk()

win.title("CS 등록 프로그램")

win.resizable(False, False)

frame1 = tk.LabelFrame(win, text='기본정보 입력')
frame1.grid(row=0, column=0, padx=5, pady=5)

frame2 = tk.LabelFrame(win, text=' * 문의내용')
frame2.grid(row=1, column=0, padx=5, pady=5)

frame3 = tk.LabelFrame(win, text='CS 채널 선택')
frame3.grid(row=2, column=0, padx=5, pady=5)

frame4 = tk.LabelFrame(win, text=' * 처리 담당자 지정 (※ 슬랙 알림 발송)')
frame4.grid(row=3, column=0, padx=5, pady=5)

frame5 = tk.LabelFrame(win, text=' * 처리 상태 ')
frame5.grid(row=4, column=0, padx=5, pady=5)

frame6 = tk.LabelFrame(win, text='CS 등록하기')
frame6.grid(row=5, column=0, padx=5, pady=5)

#=====================================
# 전역/날짜 변수
now = str(datetime.datetime.now())
today = str(datetime.date.today())
day_of_week = str(datetime.date.today().strftime("%A"))     # 영문 요일

total_date = today + " " + day_of_week

#token = 'xoxp-3917885633-113133424242-566008421730-f54b93ee06b701825d46e40c276364c8'       # 만료된 토큰 1
token = 'xoxp-3917885633-113133424242-573146862631-30b1b9e7d9531b32f20e582409895f09'

sc = SlackClient(token)

# hero_states = [hero_state_0, hero_state_1, hero_state_2, hero_state_3, hero_state_4, hero_state_5, hero_state_6]
# hero_list = ['Dave', 'Smith', 'Theo', 'Dorothy', 'Lewyn', 'Bella', 'Paul']
hero_codes = ['<@U3B3XCG74>', '<@U891L2SUS>', '<@UDVCMQN5A>', '<@U5UTV83DW>', '<@U93KUCV27>', '<@UDRQ9JHN2>', '<@UGM6EAYHW>']

slack_channel_list = ['cs_오류처리', 'cs_설치이슈', 'cs_장비이슈', 'cs_철수요청', 'cs_알림톡등록_병원명', 'cs_기타문의' ]

value_1 = list()        # 처리담당자 값을 담는 배열

codes_1 = list()        # hero_code 값을 담는 배열

#=====================================
# 등록하기 버튼 이벤트
def _enrollment():

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

#	if not value_1:
#		print('goodoc')
#		msg.showwarning('경고', '처리 담당자를 선택해주세요.')
#		return

	# 스프레드 시트 입력 기능
	'''
		print(receipt_date_box.get())                       # 날짜
		print(day_of_week)                                  # 요일
		print(hospital_name_box.get())                      # 병원명
		print(ask_contents.get('1.0', END).strip())         # 접수내용
		print(goodocmon_choose.get())                       # CS 접수자
		print(ocschart_name_box.get())                      # 연동차트
		print(ask_type_1_choose.get())                      # 문의유형(대)
		print(ask_type_2_choose.get())                      # 문의유형(중)
		print(cs_state.get())                               # 처리결과 상태 수집
		print(process_status)                               # 처리결과
	'''

	if cs_state.get() == 0:
		process_status = '처리중'
	elif cs_state.get() == 1:
		process_status = '처리완료'
	elif cs_state.get() == 2:
		process_status = '보류'

	day_of_week_2 = ['일요일', '월요일', '화요일', '수요일', '목요일', '금요일', '토요일']

	# 날짜 변환
	if day_of_week == 'Sunday':
		day_of_korean = day_of_week_2[0]
	elif day_of_week == 'Monday':
		day_of_korean = day_of_week_2[1]
	elif day_of_week == 'Tuesday':
		day_of_korean = day_of_week_2[2]
	elif day_of_week == 'Wednesday':
		day_of_korean = day_of_week_2[3]
	elif day_of_week == 'Thursday':
		day_of_korean = day_of_week_2[4]
	elif day_of_week =='Friday':
		day_of_korean = day_of_week_2[5]
	elif day_of_week == 'Saturday':
		day_of_korean = day_of_week_2[6]


	cs_data_list = [receipt_date_box.get(), day_of_korean, hospital_name_box.get(), ask_contents.get('1.0', END).strip(),
	                goodocmon_choose.get(),
	                ocschart_name_box.get(), ask_type_1_choose.get(), ask_type_2_choose.get(), process_status]

	ws.append_row(cs_data_list)  # 리스트 형태의 데이터를 행 단위로 데이터를 체크해서 자동으로 비어있는 다음행에 넣어줌


	# 슬랙 알림 기능
	for n in range(len(hero_list)):
		value_1.append(hero_states[n].get())    # 처리 담당자 체크박스의 상태값을 첫번째 배열에 추가한다.

		if value_1[n] == 1:
			codes_1.append(hero_codes[n])       # 체크된 이름의 hero_code를 두번째 배열에 추가한다.
												#print("선택한 담당자로 멘션 보내야함")
		else:
												# print("보내지 않음")
			pass

	# CS 채널 선택 값 가져오기
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

	message = ",".join(codes_1) + " CS가 접수되었습니다" + "\n" + hospital_name_box.get() + '_' + ocschart_name_box.get() + '_' + ask_type_2_choose.get() + '\n' + ask_contents.get('1.0', END).strip()

	sc.api_call('chat.postMessage', link_names=True, channel=channel_name, text=message, as_user=False, username='지옥에서 온 CS')

	msg.showinfo('결과', 'CS 등록이 완료되었습니다.')

	hospital_name_box.delete(0, END)  # 병원명
	ocschart_name_box.set('')  # 연동차트
	ask_type_1_choose.set('')  # 문의유형(대)
	ask_type_2_choose.set('')  # 문의유형(중)
	ask_contents.delete('1.0', END)  # 접수내용

	value_1.clear()     # 처리담당자 값을 담는 배열 초기화
	codes_1.clear()     # # hero_code 값을 담는 배열 초기화

	hospital_name_box.focus()

#=====================================
# 접수 일자
ttk.Label(frame1, text='* 접수 일자').grid(row=0, column=0, padx=0, pady=0, sticky='W')

# 접수 일자 입력 박스
receipt_date = tk.StringVar()       # 기입창에 표시할 문자열을 가져올 변수
receipt_date_box = ttk.Entry(frame1, width=17, textvariable=receipt_date)
receipt_date_box.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

receipt_date_box.insert(INSERT, today)

#-------------------------------------
# 접수자
ttk.Label(frame1, text='* CS 접수자').grid(row=0, column=3,  padx=0, pady=0, sticky='W')

# 접수자 입력 박스
goodocmon = tk.StringVar()
goodocmon_choose = ttk.Combobox(frame1, width=20, textvariable=goodocmon, state='readonly')
goodocmon_choose['values'] = ('데이브', '스미스', '테오', '도로시', '르윈', '벨라', '폴')
goodocmon_choose.grid(row=0, column=4, padx=5, pady=5, columnspan=1)
goodocmon_choose.current()

#-------------------------------------
# 병원명
ttk.Label(frame1, text='* 병원명 입력').grid(row=1, column=0, padx=0, pady=0, sticky='W')

# 병원명 입력 박스
hospital_name = tk.StringVar()
hospital_name_box = ttk.Entry(frame1, width=17, textvariable=hospital_name)
hospital_name_box.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

#-------------------------------------
# 연동차트
ttk.Label(frame1, text='* 연동 차트').grid(row=1, column=3, padx=0, pady=0, sticky='W')

# 연동차트 입력 박스
ocschart_name = tk.StringVar()
ocschart_name_box = ttk.Combobox(frame1, width=20, textvariable=ocschart_name, state='readonly')
ocschart_name_box['values'] \
	= ('의사랑', '오케이차트', '이지스', '비연동', '스마트CRM', '아이프로', '아이차트', '한의사랑', '히포크라테스', '팬차트', '해당없음')
ocschart_name_box.grid(row=1, column=4, padx=5, pady=5, columnspan=1)
ocschart_name_box.current()

#-------------------------------------
# 문의유형(대)
ttk.Label(frame1, text='* 문의 유형(대)').grid(row=2, column=0, padx=0, pady=0, sticky='W')

# 문의유형(대) 입력 박스
ask_type_1 = tk.StringVar()
ask_type_1_choose = ttk.Combobox(frame1, width=14, textvariable=ask_type_1, state='readonly')
ask_type_1_choose['values'] = ('사용중', '신청/기타', '설치시')
ask_type_1_choose.grid(row=2, column=1, padx=5, pady=5, columnspan=2)
ask_type_1_choose.current()

#-------------------------------------
# 문의유형(중)
ttk.Label(frame1, text='** 문의 유형(중)').grid(row=2, column=3, padx=0, pady=0, sticky='W')

# 문의유형(중) 입력 박스
ask_type_2 = tk.StringVar()
ask_type_2_choose = ttk.Combobox(frame1, width=20, textvariable=ask_type_2, state='readonly')
ask_type_2_choose['values'] = \
	('업그레이드 이슈', '[요청] 기능개선요청', '거치대/충전 이슈', '태블릿 이슈', '백신프로그램 이슈', '개인정보 이슈',
	 '알림톡 이슈', '접수프로그램사용 이슈', '차트 연동 이슈', '[요청] 프로그램 추가설치', '사용 미숙', '네트워크 불안정',
	 'USB통신 이슈', '의사랑 보안 이슈', 'PC환경이슈', '철수', '복합', '기타')
ask_type_2_choose.grid(row=2, column=4, padx=5, pady=5, columnspan=1)
ask_type_2_choose.current()

#-------------------------------------
# 문의 내용
#ttk.Label(win, text='* 문의 내용').grid(row=1, column=0, padx=0, pady=0, sticky='W')

# 문의 내용 입력 박스
scroll_w1 = 67
scroll_h1 = 10
ask_contents = scrolledtext.ScrolledText(frame2, width=scroll_w1, height=scroll_h1, wrap=tk.CHAR)      # => wrap option=CHAR/WORD
ask_contents.grid(row=2, column=0, columnspan=3, padx=5, pady=1, sticky='W')

#-------------------------------------
# CS 채널 선택 라디오 버튼
cs_channel_combo_row = 0
cs_channel_combo_row_2 = 1

#def _clickRadio():
#	return channel_state.get()

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

hero_list = ['데이브', '스미스', '테오', '도로시', '르윈', '벨라', '폴']

#hero_state = tk.IntVar()
hero_state_0 = tk.IntVar()
hero_state_1 = tk.IntVar()
hero_state_2 = tk.IntVar()
hero_state_3 = tk.IntVar()
hero_state_4 = tk.IntVar()
hero_state_5 = tk.IntVar()
hero_state_6 = tk.IntVar()

hero_states = [hero_state_0, hero_state_1, hero_state_2, hero_state_3, hero_state_4, hero_state_5, hero_state_6]

for col in range(7):
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

# 처리 상태 선택 콤보 박스
cs_state_combo_row = 0

#def _clickCombo_2():
	#return cs_state.get()

state_list = ['처리 중', '처리 완료', '보류']

cs_state = tk.IntVar()
#cs_state_1 = tk.IntVar()
#cs_state_2 = tk.IntVar()
#cs_state_3 = tk.IntVar()

#cs_states = [cs_state_1, cs_state_2, cs_state_3]

for col3 in range(3):
	cs_radio = tk.Radiobutton(frame5, text=state_list[col3], variable=cs_state, value=col3)
	cs_radio.grid(row=cs_state_combo_row, column=col3)
'''
cs_state_box_1 = tk.Checkbutton(frame5, text="오류처리", variable=cs_state_1)
cs_state_box_1.grid(row=cs_state_combo_row, column=0, sticky='W')
cs_state_box_1.deselect()
'''
#-------------------------------------
# CS 등록하기
#ttk.Label(win, text='* CS 등록하기').grid(row=10, column=0, sticky='W')

# CS 등록하기 버튼
action_1 = ttk.Button(frame6, text="뀨우!", command=_enrollment).grid(row=0, column=0, padx=5, pady=5)

#=====================================
#hospital_name_box.focus()
goodocmon_choose.focus()
#=====================================
win.mainloop()