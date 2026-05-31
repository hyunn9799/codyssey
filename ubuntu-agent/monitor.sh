#!/usr/bin/env bash

set -u

APP_NAME="agent-app"
APP_PORT="15034"
LOG_DIR="/var/log/agent-app"
LOG_FILE="${LOG_DIR}/monitor.log"

CPU_THRESHOLD=20
MEM_THRESHOLD=10
DISK_THRESHOLD=80

echo "====== SYSTEM MONITOR RESULT ======"
echo
echo "[HEALTH CHECK]"

if [ ! -d "$LOG_DIR" ]; then
  echo "[ERROR] Log directory not found: $LOG_DIR"
  exit 1
fi

if [ ! -w "$LOG_DIR" ]; then
  echo "[ERROR] Log directory is not writable: $LOG_DIR"
  exit 1
fi

PID=$(pgrep -f "$APP_NAME" | head -n 1 || true)

if [ -z "$PID" ]; then
  echo "Checking process '$APP_NAME'... [FAIL]"
  exit 1
else
  echo "Checking process '$APP_NAME'... [OK] (PID: $PID)"
fi

if ss -tuln | grep -q ":${APP_PORT} "; then
  echo "Checking port ${APP_PORT}... [OK]"
else
  echo "Checking port ${APP_PORT}... [FAIL]"
  exit 1
fi

echo
echo "[FIREWALL CHECK]"

if command -v ufw >/dev/null 2>&1; then
  UFW_STATUS=$(sudo ufw status 2>/dev/null | head -n 1 || true)

  if echo "$UFW_STATUS" | grep -qi "active"; then
    echo "UFW status... [OK] active"
  else
    echo "[WARNING] UFW is not active"
  fi
elif command -v firewall-cmd >/dev/null 2>&1; then
  if sudo firewall-cmd --state >/dev/null 2>&1; then
    echo "firewalld status... [OK] active"
  else
    echo "[WARNING] firewalld is not active"
  fi
else
  echo "[WARNING] No supported firewall tool found"
fi

echo
echo "[RESOURCE MONITORING]"

CPU_USAGE=$(top -bn1 | awk '/%Cpu|Cpu\(s\)/ {
  for (i=1; i<=NF; i++) {
    if ($i ~ /id/) {
      idle=$(i-1)
      usage=100-idle
      printf "%.1f", usage
      exit
    }
  }
}')

if [ -z "${CPU_USAGE:-}" ]; then
  CPU_USAGE=$(awk '/^cpu / {
    idle=$5
    total=0
    for (i=2; i<=NF; i++) total += $i
    printf "%.1f", (1 - idle/total) * 100
  }' /proc/stat)
fi

MEM_USAGE=$(free | awk '/Mem:/ {
  printf "%.1f", ($3/$2)*100
}')

DISK_USED=$(df / | awk 'NR==2 {gsub("%","",$5); print $5}')

echo "CPU Usage : ${CPU_USAGE}%"
echo "MEM Usage : ${MEM_USAGE}%"
echo "DISK Used  : ${DISK_USED}%"

echo

# 기본 쉘 스크립트트 소수점 크기 비교를 못한다
CPU_WARN=$(awk -v value="$CPU_USAGE" -v limit="$CPU_THRESHOLD" 'BEGIN {print (value > limit) ? 1 : 0}')
MEM_WARN=$(awk -v value="$MEM_USAGE" -v limit="$MEM_THRESHOLD" 'BEGIN {print (value > limit) ? 1 : 0}')

if [ "$CPU_WARN" -eq 1 ]; then
  echo "[WARNING] CPU threshold exceeded (${CPU_USAGE}% > ${CPU_THRESHOLD}%)"
fi

if [ "$MEM_WARN" -eq 1 ]; then
  echo "[WARNING] MEM threshold exceeded (${MEM_USAGE}% > ${MEM_THRESHOLD}%)"
fi

if [ "$DISK_USED" -gt "$DISK_THRESHOLD" ]; then
  echo "[WARNING] DISK threshold exceeded (${DISK_USED}% > ${DISK_THRESHOLD}%)"
fi

rotate_log() {
  if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(stat -c%s "$LOG_FILE")

    if [ "$LOG_SIZE" -ge 10485760 ]; then
      for i in $(seq 9 -1 1); do
        if [ -f "${LOG_FILE}.${i}" ]; then
          mv "${LOG_FILE}.${i}" "${LOG_FILE}.$((i + 1))"
        fi
      done

      mv "$LOG_FILE" "${LOG_FILE}.1"
      touch "$LOG_FILE"
      chmod 660 "$LOG_FILE"
    fi
  fi
}

rotate_log

NOW=$(date '+%Y-%m-%d %H:%M:%S')
LOG_LINE="[${NOW}] PID:${PID} CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK_USED:${DISK_USED}%"

echo "$LOG_LINE" >> "$LOG_FILE"

echo
echo "[INFO] Log appended: $LOG_FILE"