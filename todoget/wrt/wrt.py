from datetime import date, datetime

def create_header():
    title = "Todoget"
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    header = '---' + '\n' + 'title: ' + title + '\n' + 'date: ' + str(date.today()) + ' ' + '(' + current_time  + ')' + '\n' + '---' + '\n'
    return header

def create_file_title(filename):
    title = '\n' + "#" + " " + filename + '\n'
    return title
	
def format_line(line, number):
	line_new = '- ' + "Line " + str(number) + ":" + ' ' +line
	return line_new

def rep_string(string, times, sep = ""):
	out = [string]
	out = out * times
	out = sep.join(out)
	return(out)