import tkinter
from tkinter import ttk
from tkinter import messagebox

# 비트레이트
LIST_RATE = [50, 400, 800, 1200, 2000]

"""
입력 콘솔
"""
def initialize_data(input):

	ret = {}
	if input == "train":
		box = tkinter.Tk()
		box.title("Data Input")

		tkinter.Label(box, text="UE 수를 입력하시오").pack()
		NUM_UE = tkinter.StringVar(box, value='3')
		ttk.Entry(box, textvariable = NUM_UE).pack()

		tkinter.Label(box, text="AP 수를 입력하시오").pack()
		NUM_AP = tkinter.StringVar(box, value='2')
		ttk.Entry(box, textvariable = NUM_AP).pack()

		tkinter.Label(box, text="UE - AP의 연결률을 입력하시오(%)").pack()
		PERCENT_CONNECT = tkinter.StringVar(box, value='100')
		ttk.Entry(box, textvariable = PERCENT_CONNECT).pack()

		tkinter.Label(box, text="Timeslot 값을 입력하시오").pack()
		VAL_TIMESLOT = tkinter.StringVar(box, value='1.0')
		ttk.Entry(box, textvariable = VAL_TIMESLOT).pack()

		tkinter.Label(box, text="Bandwidth 평균 값을 입력하시오").pack()
		BW_AVG = tkinter.StringVar(box, value='2000')
		ttk.Entry(box, textvariable = BW_AVG).pack()

		tkinter.Label(box, text="Bandwidth 표준편차 값을 입력하시오").pack()
		BW_STD = tkinter.StringVar(box, value='500')
		ttk.Entry(box, textvariable = BW_STD).pack()

		ret = {}
	
		def parse_data():
			try:
				# 입력으로 받는 것들
				ret['NUM_UE'] = int(NUM_UE.get())
				ret['NUM_AP'] = int(NUM_AP.get())
				ret['PERCENT_CONNECT'] = int(PERCENT_CONNECT.get())
				ret['VAL_TIMESLOT'] = float(VAL_TIMESLOT.get())
				ret['BW_AVG'] = float(BW_AVG.get())
				ret['BW_STD'] = float(BW_STD.get())
	
				if ret['NUM_UE'] <= 0:
					messagebox.showerror("Error", "Please check your input")
				elif ret['NUM_AP'] <= 0:
					messagebox.showerror("Error", "Please check your input")
				elif ret['PERCENT_CONNECT'] <= 0 or ret['PERCENT_CONNECT'] > 100:
					messagebox.showerror("Error", "Please check your input")
				elif ret['VAL_TIMESLOT'] <= 0:
					messagebox.showerror("Error", "Please check your input")
				elif ret['BW_AVG'] <= 0:
					messagebox.showerror("Error", "Please check your input")
				elif ret['BW_STD'] <= 0:
					messagebox.showerror("Error", "Please check your input")
				else:
					file = open("configure.txt", "w")
					file.write("NUM_UE | %d\n" % ret['NUM_UE'])
					file.write("NUM_AP | %d\n" % ret['NUM_AP'])
					file.write("PERCENT_CONNECT | %d\n" % ret['PERCENT_CONNECT'])
					file.write("VAL_TIMESLOT | %d\n" % ret['VAL_TIMESLOT'])
					file.write("BW_AVG | %d\n" % ret['BW_AVG'])
					file.write("BW_STD | %d\n" % ret['BW_STD'])
					file.write("END")
					file.close()
					box.destroy()
			except ValueError:
				messagebox.showerror("Error", "Please check your input")

		action = ttk.Button(box, text="Enter", command = parse_data)
		action.pack()
		box.mainloop()
	else:
		file = open("configure.txt", "r")
		lines = file.readlines()
		ret['NUM_UE'] = int(lines[0].split("|")[1].strip())
		ret['NUM_AP'] = int(lines[1].split("|")[1].strip())
		ret['PERCENT_CONNECT'] = int(lines[2].split("|")[1].strip())
		ret['VAL_TIMESLOT'] = float(lines[3].split("|")[1].strip())
		ret['BW_AVG'] = int(lines[4].split("|")[1].strip())
		ret['BW_STD'] = int(lines[5].split("|")[1].strip())
		file.close()

	# 전역 변수로 지정한 것들
	ret['LIST_RATE'] = LIST_RATE
	ret['NUM_RATE'] = len(LIST_RATE)
	
	return ret