import time

# 실행 시간 측정 시작
start_time = time.perf_counter()

print("Hello?")

# 실행 시간 측정 종료
end_time = time.perf_counter()

# 실행 시간 출력
execution_time = end_time - start_time
print(f"실행 시간: {execution_time:.4f}초")