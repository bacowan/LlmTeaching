# extracts the conversation that the student would see from the log file
import os

log_file = "./chat_logs_list_reverse_2.log"
split_file = os.path.splitext(log_file)
new_log_file = split_file[0] + "_conversation" + split_file[1]

include_log_types = ("INFO:root:VisibleQuestion:", "INFO:root:VisibleResponse:", "INFO:root:New Conversation")
log_start = "INFO:root:"

with open(log_file, "r") as f:
    lines = f.readlines()

with open(new_log_file, 'a') as the_file:
    show_current_line = False
    for line in lines:
        if line.startswith(log_start):
            show_current_line = line.startswith(include_log_types)
        if (show_current_line):
            the_file.write(line)