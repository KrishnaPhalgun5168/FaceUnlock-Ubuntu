import pyautogui
with open('output.txt', 'r') as file:
	password=file.read().replace('\n', '')
	#print(password, len(password))
	pyautogui.typewrite(password)
	pyautogui.press('enter')
	print('unlocked')