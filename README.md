# Statistics Parser
Парсер статистики из excel файла определенного формата
<details>
<summary>Подробнее ...</summary>
Создать парсер excel файла (см. ниже) на Python

Создать таблицу согласно нормам реляционных баз данных (внести все значения в одну таблицу)

Добавить расчетный тотал по Qoil, Qliq, сгруппированный по датам (даты можете указать свои, добавив программно, не изменяя исходный файл, при условии, что дни будут разные, а месяц и год одинаковые)

Пример excel файла:
<table>
    <tr><th rowspan="3">id</th><th rowspan="3">company</th><th colspan="4">fact</th><th colspan="4">forecast</th></tr>
    <tr><th colspan="2">Qliq</th><th colspan="2">Qoil</th><th colspan="2">Qliq</th><th colspan="2">Qoil</th></tr>
    <tr><th>data1</th><th>data2</th><th>data1</th><th>data2</th><th>data1</th><th>data2</th><th>data1</th><th>data2</th></tr>
    <tr><td>1</td><td>company1</td><td>10</td><td>20</td><td>30</td><td>40</td><td>12</td><td>22</td><td>15</td><td>25</td></tr>
    <tr><td>2</td><td>company2</td><td>11</td><td>21</td><td>31</td><td>41</td><td>13</td><td>23</td><td>20</td><td>30</td></tr>
    <tr><td>3</td><td>company1</td><td>12</td><td>22</td><td>32</td><td>42</td><td>14</td><td>24</td><td>25</td><td>35</td></tr>
    <tr><td>4</td><td>company2</td><td>13</td><td>23</td><td>33</td><td>43</td><td>15</td><td>25</td><td>30</td><td>40</td></tr>
    <tr><td>5</td><td>company1</td><td>14</td><td>24</td><td>34</td><td>44</td><td>16</td><td>26</td><td>35</td><td>45</td></tr>
    <tr><td>6</td><td>company2</td><td>15</td><td>25</td><td>35</td><td>45</td><td>17</td><td>27</td><td>40</td><td>50</td></tr>
    <tr><td>7</td><td>company1</td><td>16</td><td>26</td><td>36</td><td>46</td><td>18</td><td>28</td><td>45</td><td>55</td></tr>
    <tr><td>8</td><td>company2</td><td>17</td><td>27</td><td>37</td><td>47</td><td>19</td><td>29</td><td>50</td><td>60</td></tr>
    <tr><td>9</td><td>company1</td><td>18</td><td>28</td><td>38</td><td>48</td><td>20</td><td>30</td><td>55</td><td>65</td></tr>
    <tr><td>10</td><td>company2</td><td>19</td><td>29</td><td>39</td><td>49</td><td>21</td><td>31</td><td>60</td><td>70</td></tr>
    <tr><td>11</td><td>company1</td><td>20</td><td>30</td><td>40</td><td>50</td><td>22</td><td>32</td><td>65</td><td>75</td></tr>
    <tr><td>12</td><td>company2</td><td>21</td><td>31</td><td>41</td><td>51</td><td>23</td><td>33</td><td>70</td><td>80</td></tr>
    <tr><td>13</td><td>company1</td><td>22</td><td>32</td><td>42</td><td>52</td><td>24</td><td>34</td><td>75</td><td>85</td></tr>
    <tr><td>14</td><td>company2</td><td>23</td><td>33</td><td>43</td><td>53</td><td>25</td><td>35</td><td>80</td><td>90</td></tr>
    <tr><td>15</td><td>company1</td><td>24</td><td>34</td><td>44</td><td>54</td><td>26</td><td>36</td><td>85</td><td>95</td></tr>
    <tr><td>16</td><td>company2</td><td>25</td><td>35</td><td>45</td><td>55</td><td>27</td><td>37</td><td>90</td><td>100</td></tr>
    <tr><td>17</td><td>company1</td><td>26</td><td>36</td><td>46</td><td>56</td><td>28</td><td>38</td><td>95</td><td>105</td></tr>
    <tr><td>18</td><td>company2</td><td>27</td><td>37</td><td>47</td><td>57</td><td>29</td><td>39</td><td>100</td><td>110</td></tr>
    <tr><td>19</td><td>company1</td><td>28</td><td>38</td><td>48</td><td>58</td><td>30</td><td>40</td><td>105</td><td>115</td></tr>
    <tr><td>20</td><td>company2</td><td>29</td><td>39</td><td>49</td><td>59</td><td>31</td><td>41</td><td>110</td><td>120</td></tr>
</table></details>

<hr>

## Как запустить на локальном компьютере?

### Клонировать проект из репозитория GitHub

```bash
git clone https://github.com/KotelnikovKP/statistic-parser.git 
```

### Установить виртуальное окружение

Выполните следующие команды (убедитесь, что на локальном компьютере установлен pyton)

```bash
python -m venv venv
#OR
python3 -m venv venv

```

### Активируйте виртуальное окружение

```bash
# Windows
venv/Scripts/activate

# MacOs + Linux
source venv/bin/activate
```

### Установите зависимости

Убедитесь, что находитесь в директории проекта

```bash
pip install -r requirements.txt
```

### Запустите сервер Django


```bash
python manage.py runserver
```

### Запустите приложение


```bash
http://127.0.0.1:8000/

```

