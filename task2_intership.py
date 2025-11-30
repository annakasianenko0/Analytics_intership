import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns  

df = pd.read_csv("/Users/anakasanenko/Task2_intership/data_task2.csv")  
#print(df.head())

# Змінюємо строки на datetime
df['request_time'] = pd.to_datetime(df['request_time'])
df['start_time'] = pd.to_datetime(df['start_time'])
df['finish_time'] = pd.to_datetime(df['finish_time'])

# Метрики 
df['sla_wait']   = (df['start_time']  - df['request_time']).dt.total_seconds() / 60
df['handling']   = (df['finish_time'] - df['start_time']).dt.total_seconds() / 60
df['total_time'] = (df['finish_time'] - df['request_time']).dt.total_seconds() / 60

df['sla_ok']       = df['sla_wait']   <= 5
df['handling_ok']  = df['handling']   <= 15
df['total_ok']     = df['total_time'] <= 45

print("Загальні показники")
print(" ")

print("\nМедіанне значення метрик:")
print(df[['sla_wait','handling','total_time']].median())
print(" ")

print("\nДоля виконання SLA:")
print(df[['sla_ok','handling_ok','total_ok']].mean())
print(" ")

print("ПОРІВНЯННЯ КОМАНД")

print("\nСередній час обробки:")
print(df.groupby('team')[['sla_wait','handling','total_time']].median())
print(" ")

print("\nДоля виконання SLA по командам:")
print(df.groupby('team')[['sla_ok','handling_ok','total_ok']].mean())
print(" ")

#Графік Медіанне значення часу очікування по командам
df.groupby('team')['sla_wait'].median().plot.bar()
plt.title("Медіанне значення часу очікування по командам")
plt.ylabel("Хвилини")
plt.show()

#Графік Медіанне значення часу обробки однієї заявки по командам
df.groupby('team')['handling'].median().plot.bar()
plt.title("Медіанне значення часу обробки однієї заявки по командам")
plt.ylabel("Хвилини")
plt.show()

#Графік Медіанне значення загально використаного часу на обробку заявки по командам
df.groupby('team')['total_time'].median().plot.bar()
plt.title("Медіанне значення загально використаного часу на обробку заявки по командам")
plt.ylabel("Хвилини")
plt.show()

print("\nТОП-5 ШВИДКИХ АГЕНТІВ")
print(df.groupby('moderator')['handling'].median().sort_values().head(5))
print(" ")

print("\nТОП-5 НАЙПОВІЛЬНІШИХ АГЕНТІВ")
print(df.groupby('moderator')['handling'].median().sort_values().tail(5))
print(" ")


top_fast = df.nsmallest(10, 'total_time')[['moderator', 'total_time', 'request_time', 'team']]
labels_fast = top_fast['moderator'].astype(str) + " (" + top_fast['team'].astype(str) + ") " + top_fast['request_time'].dt.strftime('%Y-%m-%d')

print("\nТОП 10 САМИХ ШВИДКИХ РОЗГЛЯДІВ за (total_time):")
print(" ")
print(top_fast)
print(" ")

plt.figure(figsize=(10,5))
plt.barh(labels_fast, top_fast['total_time'])
plt.title("ТОП 10 САМИХ ШВИДКИХ РОЗГЛЯДІВ за (total_time)")
plt.xlabel("Загальний час обробки в (хв)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()


print(" ")
# Фільтруємо кейси з total_time > 45 хвилин
slow_cases = df[df['total_time'] > 45][['moderator', 'total_time', 'request_time', 'team']]

print(f"Всього дуже повільних кейсів, де total_time > 45: {len(slow_cases)}")
print(" ")
total_cases = len(df)
print(f"Всього кейсів:{total_cases}")
print(" ")

print("ТОП 20 САМИХ ПОВІЛЬНИХ РОЗГЛЯДІВ")
print(" ")
top_slow = slow_cases.sort_values(by = 'total_time', ascending= False).head(20)

print(top_slow) 
print(" ")

labels_slow = top_slow['moderator'].astype(str) + " (" + top_slow['team'].astype(str) + ") " + top_slow['request_time'].dt.strftime('%Y-%m-%d')

# Малюємо графік
plt.figure(figsize=(12,6))
plt.barh(labels_slow, top_slow['total_time'])
plt.title("Топ-20 кейсів з total_time > 45 хвилин")
plt.xlabel("Загальний час обробки (хв)")
plt.gca().invert_yaxis()  
plt.tight_layout()
plt.show()



#Графік Кількість розглянутих кейсів по агентам в день
df['date'] = df['request_time'].dt.date

print("Кількість розглянутих кейсів по агентам в день")
print(df.groupby(['moderator','date']).size().reset_index(name='cases'))
print(" ")

cases_df = df.groupby(['moderator', 'date']).size().reset_index(name='cases')
pivot_df = cases_df.pivot(index='date', columns='moderator', values='cases')


pivot_df = df.groupby(['date', 'moderator']).size().unstack(fill_value=0)


plt.figure(figsize=(10,5))
df['handling'].plot.hist(bins=50)
plt.title("Розподіл часу обробки")
plt.xlabel("Хвилини")
plt.show()

#Графік Розподіл заявок по годинах
df['hour'] = df['request_time'].dt.hour
cases_per_hour = df.groupby('hour').size()

plt.figure(figsize=(10,4))
cases_per_hour.plot(kind='bar')
plt.title('Розподіл заявок по годинах')
plt.xlabel('Година')
plt.ylabel('Кількість заявок')
plt.tight_layout()
plt.show()

#Графік Розподіл заявок по днях тижня
df['weekday'] = df['request_time'].dt.day_name()

cases_per_weekday = df.groupby('weekday').size().reindex(
    ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'])

plt.figure(figsize=(10,4))
cases_per_weekday.plot(kind='bar')
plt.title('Розподіл заявок по днях тижня')
plt.xlabel('День тижня')
plt.ylabel('Кількість заявок')
plt.tight_layout()
plt.show()

