"""
version : v1.0.3

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


def check_folder(current_timestamp, folders):
    results = [0]

    report_message = '* Dropper API Log Custodian Report *\n\n\n'

    for folder in folders:
        try:
            if os.path.exists(folder):
                results.append([0, {'size': sum(os.path.getsize(folder + '/' + file) for file in os.listdir(folder) if os.path.isfile(folder + '/' + file))/(1024*1024*1024)}])
            else:
                if results[0] < 1:
                    results[0] = 1
                os.makedirs(folder)
                results.append([1, {'message': 'Folder Created', 'size': sum(os.path.getsize(folder + '/' + file) for file in os.listdir(folder) if os.path.isfile(folder + '/' + file))/(1024*1024*1024)}])
        except Exception as ex:
            if results[0] < 2:
                results[0] = 2
            results.append([2, {'message': ex, 'size': 0}])

    for result, i in zip(results[1:], range(len(folders))):
        report_message += f"[{folders[i]}] {'GREEN' if result[0]==0 else 'YELLOW' if result[0]==1 else 'RED'}\n"
        
        if result[0] == 0:
            report_message += '---------------------------\n'
            report_message += f"size:\n{result[1]['size']}GB\n"
            report_message += '---------------------------\n'
        elif result[0] == 1:
            report_message += '---------------------------\n'
            report_message += f"{result[1]['message']}\n\nsize:\n{result[1]['size']}GB\n"
            report_message += '---------------------------\n'
        elif result[0] == 2:
            report_message += '---------------------------\n'
            report_message += f"{result[1]['message']}\n"
            report_message += '---------------------------\n'
        report_message += '\n'

    report_message += '\n\n'
    report_message += f"total size: {sum(data[1]['size'] for data in results[1:])}GB"

    if results[0] == 0:
        report_message += '\n\n\n\n\n'
        report_message += 'Operating finished successfully\n'
    elif results[0] == 1:
        report_message += '\n\n\n\n\n'
        report_message += 'Error has been fixed automatically\n'
    else:
        report_message += '\n\n\n\n\n'
        report_message += 'Some error occurred while crawling\n'

    report_message += '\nThis report is based on (Unix Time)' + str(int(current_timestamp))

    if results[0] == 0:
        mail_sender.send_mail(
            subject=f'[Dropper API](api-log-custodian) INFO: task report',
            message=report_message)
    elif results[0] == 1:
        mail_sender.send_mail(
            subject=f'[Dropper API](api-log-custodian) WARN: task report',
            message=report_message)
    else:
        mail_sender.send_mail(
            subject=f'[Dropper API](api-log-custodian) ERROR: task report',
            message=report_message)



if __name__ == '__main__':
    timestamp = int(time.time())

    folder_list = ['log', 'foreign-data', 'status-data']

    check_folder(timestamp, folder_list)
