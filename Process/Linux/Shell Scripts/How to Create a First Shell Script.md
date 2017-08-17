## 学习 Shell Scripts！！！


LINFO 
How to Create a First Shell Script



Shell scripts are short programs that are written in a shell programming language and interpreted by a shell process. They are extremely useful for automating tasks on Linux and other Unix-like operating systems.

A shell is a program that provides the traditional, text-only user interface for Unix-like operating systems. Its primary function is to read commands (i.e., instructions) that are typed into a console (i.e., an all-text display mode) or terminal window (i.e., all-text mode window) and then execute (i.e., run) them. The default shell on Linux is the very commonly used and highly versatile bash.

A programming language is a precise, artificial language that is used to write computer programs, which are sets of instructions that can be automatically translated (i.e., interpreted or compiled) into a form (i.e., machine language) that is directly understandable by a computer's central processing unit (CPU).

A feature of bash and other shells used on Unix-like operating systems is that each contains a built-in programming language, referred to as a shell programming language or shell scripting language, which is used to create shell scripts. Among the advantages of using shell scripts are that they can be very easy to create and that a large number are already available in books and on the Internet for use with or without modification for a wide variety of tasks. Shell scripts are also employed extensively in the default installations of Unix-like operating systems.

A First Script

The following example, although extremely simple, provides a useful introduction to creating and using shell scripts. The script clears the monitor screen of all previous lines and then writes the text Good morning, world. on it.

All that is necessary to create this script is to open a text editor (but not a word processor), such as gedit or vi, and type the following three lines exactly as shown on a new, blank page:

#!/bin/bash
clear
echo "Good morning, world."

Alternatively, the above code could be copied from this page and pasted to a blank page opened by the text editor page using the standard keyboard or mouse copy and paste functions.

After saving this plain text file, with a file name such as morning (or anything else desired), the script is complete and almost ready to run. Scripts are typically run by typing a dot, a forward slash and the file name (with no spaces in between) and then pressing the ENTER key. Thus, for example, if the above script were saved with the name morning, an attempt could be made to execute it by issuing the following command:

./morning

However, the script probably will not run, in which case an error message will appear on the screen such as bash: ./morning: Permission denied. This is because the permissions for the file first have to be set to executable. (By default, the permissions for new files are set to read and write only.) The problem can easily be solved by using the chmod command with its 755 option (which will allow the file creator to read, write and execute the file) while in the same directory as that in which the file is located as follows:

chmod 755 morning

Now the script is ready to run by typing the following, again while in the same directory, and then pressing the ENTER key:

./morning


How It Works

The first of the three lines tells the operating system what shell to use to interpret the script and the location (i.e., absolute pathname) of the shell. The shell is bash, which is located in the /bin directory (as are all shells); thus the line contains /bin/bash. This instruction is always preceded by a pound sign and an exclamation mark in order to inform the operating system that it is providing the name and location of the shell (or other scripting language).

The second line tells the shell to issue the clear command. This is a very simple command that removes all previous commands and output from the console or terminal window in which the command was issued.

The third line tells the shell to write the phrase Good morning, world. on the screen. It uses the echo command, which instructs the shell to repeat whatever follows it. (The quotation marks are not necessary in this case; however, it is good programming practice to use them, and they can make a big difference in more advanced scripts.) In slightly more technical terms, Good morning, world. is an argument (i.e., input data) that is passed to the echo command.

As is the case with other commands used in shell scripts, clear and echo can also be used independently of scripts. Thus, for example, typing clear on the screen and pressing the ENTER key would remove all previous commands and output and just leave a command prompt for entering the next command.

It Doesn't Work!

If the phrase Good morning, world. does not appear at the top of the screen, there are several possible reasons: (1) an error was made in copying the code (such as omitting the word echo), (2) the name used in the command was not exactly the same as that of the file (e.g., there is an extra space or a minor difference in spelling or capitalization), (3) the period and/or forward slash were omitted (or reversed) in the command, (4) a space was inserted after the period or slash, (5) the file is not a plain text file (typically because a word processor was used to create it instead of a text editor), (6) the command was not issued in the same directory as that in which the file is located and (7) the permissions were not changed to execute for the owner (i.e., creator) of the file.

It is important to avoid practicing writing and executing scripts as the root (i.e., administrative) user. An improperly written script could damage the operating system, and, in a worst case scenario, it could result in the loss of valuable data and make it necessary to reinstall the entire operating system. For this and other reasons, if an ordinary user account does not yet exist on the computer, one should immediately be created (which can be easily accomplished with a command such as adduser).

Experiments

There are a number of simple, and instructive, experiments that a curious user could do with the above example before moving on to more complex examples. They consist of revising the code as suggested below, saving the revisions (using either the same file name or a different file name), and then executing them as explained above.

(1) One is to try changing some of the wording (for example, changing the third line to echo "Good evening, folks.").

(2) Another is to add one or more additional lines to be written to the screen, each beginning with the word echo followed by at least one horizontal space.

(3) A third is to leave a blank line between two echo lines. (It will be seen that this will not affect the result; however, a blank line can be created by just typing echo on it and nothing else.)

(4) A fourth is to insert some blank horizontal spaces. (Notice that the result will be different depending on whether the blank spaces are inserted before or after the first quotation marks. This tells something about the role of quotation marks in shell scripts.)

(5) A fifth is to execute the file from a different directory from that in which it is located. This requires adding the path of the executable script to the beginning of the command name when it is issued (e.g., ./test/morning if the file has been moved to a subdirectory named test).

(6) Another experiment would be to add some other command to the script file, such as ps (which shows the processes currently on the system), pwd (which shows the current directory), uname (which provides basic information about a system's software and hardware) or df (which shows disk space usage). (Notice that these and other commands can be used in the script with any appropriate options and/or arguments.)










Created December 21, 2005.
Copyright © 2005 The Linux Information Project. All Rights Reserved.

