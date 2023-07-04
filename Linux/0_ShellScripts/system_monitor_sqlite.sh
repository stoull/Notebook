#!/bin/bash
cpu=$(</sys/class/thermal/thermal_zone0/temp)
cputemp=$((cpu/1000))
gputemp=$(/opt/vc/bin/vcgencmd measure_temp | sed "s/[^0-9.]//g")
cpufrequency=$(/opt/vc/bin/vcgencmd measure_clock arm)
cpu_used_rate=$(top -b -d1 -n1|grep -i "Cpu(s)"|head -c21|cut -d ' ' -f3|cut -d '%' -f1)
memery_used_rate=$(free | awk 'FNR == 3 {print $3/($3+$4)*100}')
systme_uptime=$(uptime -p)
cpufrequency=${cpufrequency//frequency(48)=/}
sqlite3 /home/pi/Desktop/system_monitor/system_log << EOF
select * from System;
INSERT INTO System (date, core_frequency, cpu_temp, gpu_temp, cpu_rate, memory_rate, sys_run_time)
VALUES (DATETIME(), "$cpufrequency", "$cputemp", "$gputemp", "$cpu_used_rate", "$memery_used_rate", "$systme_uptime");
EOF
