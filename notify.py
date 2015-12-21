from sage import get_grades
import sendgrid
from secrets import sendgrid_pass,sendgrid_user
from time import sleep
import selenium

def print_grades(l):
    for tup in l:
        print "{0:36}: {1}".format(*tup)

if __name__=='__main__':
    sg = sendgrid.SendGridClient(sendgrid_user,sendgrid_pass)

    initial = get_grades()
    print_grades(initial) 
    failed = False
    while True:
        if not failed:
            sleep(60*5)
        failed = False
        try:
            new = get_grades()
            diff = set(new) - set(initial)
            if len(diff)>0:
                message = sendgrid.Mail()
                message.add_to("Arya <aboudaie@brandeis.edu>")
                message.set_subject('Grade Changed')
                message.set_text('Added Grade: {}'.format(str(diff)))
                message.set_from('Arya Boudaie <aboudaie@brandeis.edu>')
                status, msg = sg.send(message)
                print_grades(new) 
                initial=new
        except selenium.common.exceptions.NoSuchElementException as e:
            failed = True #I don't really care if it fails once
        
