import selenium
from selenium import webdriver


class GroupRoomReservation:

	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.driver = webdriver.Chrome()

	def login(self):
		self.driver.get('https://cloud.timeedit.net/chalmers/web/b1/')
		
		assert 'TimeEdit - Chalmers' in self.driver.title

		# Log in to TimeEdit via Chalmer's IDP
		self.driver.find_element_by_id('loginForm').click()

		# Fill in username and password
		username = self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_UsernameTextBox')
		username.send_keys(self.username)

		password = self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_PasswordTextBox')
		password.send_keys(self.password)

		self.driver.find_element_by_id('ctl00_ContentPlaceHolder1_SubmitButton').click()

	def book_group_room(self, room):
		# Select "Boka"
		self.driver.find_element_by_class_name('greenlink').click()

		# Fill in room number
		r = self.driver.find_element_by_xpath("/html/body/div[16]/div/div[3]/form/fieldset[1]/div/table/tbody/tr[1]/td[2]/input[1]")
		r.send_keys(room)

		for i in [3, 4, 5, 6]:
			try:
				booking = self.driver.find_element_by_xpath("/html/body/div[16]/div/div[4]/div/table/tbody/tr[%d]/td[2]" % i)
				print(booking.get_attribute("innerText"))
			except selenium.common.exceptions.NoSuchElementException:
				pass

	def close(self):
		self.driver.close()


if __name__ == "__main__":
	username = ''
	password = ''

	time_edit = GroupRoomReservation(username, password)
	time_edit.login()
	time_edit.book_group_room('F4057')

	time_edit.close()
