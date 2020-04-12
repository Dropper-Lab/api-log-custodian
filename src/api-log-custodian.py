"""
MIT License

Copyright (c) 2020 Dropper Lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os
import time

import mail_sender


def check_folder(folders):
    errors = [0]

    for folder in folders:
        try:
            if not os.path.exists(folder):
                os.makedirs(folder)
        except Exception as ex:
            errors[0] = 1
            errors.append([ex, folder])

    return errors


if __name__ == '__main__':
    timestamp = int(time.time())

    folder_list = ['log', 'foreign-data', 'status-data']

    error_list = check_folder(folder_list)

    report_message = '* Dropper API Log Custodian Report *\n\n\n'

    if error_list[0] == 0:
        report_message += 'Operating finished successfully\n'
    else:
        for error in error_list[1:]:
            report_message += '---------------------------\n'
            report_message += f"{error[0]}\n\nfolder:\n{error[1]}\n"
        report_message += '---------------------------\n'
        report_message += '\n\n\n\n\n'
        report_message += 'Some error occurred while crawling\n'

    report_message += '\nThis report is based on (Unix Time)' + str(int(timestamp))

    if error_list[0] == 0:
        mail_sender.send_mail(
            subject=f'[Dropper API](api-log-custodian) INFO: task report',
            message=report_message)
    else:
        mail_sender.send_mail(
            subject=f'[Dropper API](api-log-custodian) ERROR: task report',
            message=report_message)
