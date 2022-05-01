# -*- coding: utf-8 -*-

import json
from bs4 import BeautifulSoup
import base64
import re 
import asyncio
import aiohttp


async def get_room(taskHash):
    url = f"https://api-edu.skysmart.ru/api/v1/task/preview"
    payload = "{\"taskHash\":\"" + taskHash + "\"}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NTE0MDI2MzMsImV4cCI6MTY1Mzk5NDYzMywicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJhdXRoVXNlcklkIjpudWxsLCJ1c2VySWQiOjM3Nzg4NjQ3LCJlbWFpbCI6InRlc3RpbGluZXRlc3RAZ21haWwuY29tIiwibmFtZSI6ItCf0JDQktCe0JDQotCf0J7QktCi0JDQnyIsInN1cm5hbWUiOiLQq9CS0JDQn9Cr0JLQkNCf0KvQktCQIiwiaWRlbnRpdHkiOiJiYWZlZHVuYWdlIn0.YgHn0lJEYmXLmn3g8vFl7NN5awMrf9S7diDhP3wsu9A_4BLzGY6YQqYHZrt-dfGFRcGUHsmrwTOl-QgTQ_gSspL-NYE3DADs0IzbDrwRpL4LD2rSDM016LH4pS2-TqHknV-KN1lX49kva55JUEQzmpzNkKtJtnGluRaBSX83misEfjYcyM0RNxVSaCP89hP0r-dSd80e8eylvdveh0TrOrEuPQAlN9bBJCHPvGgRlxbGxvi0OBPeBd6_wS_vBf9JP4WIjmNaSi1CV0ddijlDcb42DhNFrmkV8CA_0-R63MCH0DxX5hd5igisd726Yijz_bK_dYkSxbCa0FN_W2mDb41W5xBx2BU7jd2DMz6250B7ceZo_Y3FHSZ9G2EkHVrKuoUxaFXmXUfHOxlcynH2tbUSMBVTW9nZwEzQh8Rmf-p5UuNStmilfqIrLGPz8LQx5_-LBbgusQK6pjbsesCwicsM6KN-jA1E45iqufe1OfebEYzyfEGRVnFwNlCNWuGR5PY0263W-vo-tupzR0UHmjT8PD73WE-UjprTm_gPpfu9ZjCG82jdalrbmZv-d72pEd5YaBW9BSrtw2FvaFHM0IZXfIsP79MjNmXPay68pmlMiSV8bimVzgEBlmek3rC6gLGmNkURN0OQrWWCcoW8g6EMfJ3NcjUVPKi3OajdH5w',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Accept:': 'application/json, text/plain, */*'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, data=payload) as resp:
            steps_raw = await resp.json() 
            print(steps_raw)
            await session.close()
            return steps_raw['meta']['stepUuids'] # все uuid заданий
            
async def get_json_html(uuid):
    url = "https://api-edu.skysmart.ru/api/v1/content/step/load?stepUuid=" + uuid
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2NTE0MDI2MzMsImV4cCI6MTY1Mzk5NDYzMywicm9sZXMiOlsiUk9MRV9FRFVfU0tZU01BUlRfU1RVREVOVF9VU0FHRSJdLCJhdXRoVXNlcklkIjpudWxsLCJ1c2VySWQiOjM3Nzg4NjQ3LCJlbWFpbCI6InRlc3RpbGluZXRlc3RAZ21haWwuY29tIiwibmFtZSI6ItCf0JDQktCe0JDQotCf0J7QktCi0JDQnyIsInN1cm5hbWUiOiLQq9CS0JDQn9Cr0JLQkNCf0KvQktCQIiwiaWRlbnRpdHkiOiJiYWZlZHVuYWdlIn0.YgHn0lJEYmXLmn3g8vFl7NN5awMrf9S7diDhP3wsu9A_4BLzGY6YQqYHZrt-dfGFRcGUHsmrwTOl-QgTQ_gSspL-NYE3DADs0IzbDrwRpL4LD2rSDM016LH4pS2-TqHknV-KN1lX49kva55JUEQzmpzNkKtJtnGluRaBSX83misEfjYcyM0RNxVSaCP89hP0r-dSd80e8eylvdveh0TrOrEuPQAlN9bBJCHPvGgRlxbGxvi0OBPeBd6_wS_vBf9JP4WIjmNaSi1CV0ddijlDcb42DhNFrmkV8CA_0-R63MCH0DxX5hd5igisd726Yijz_bK_dYkSxbCa0FN_W2mDb41W5xBx2BU7jd2DMz6250B7ceZo_Y3FHSZ9G2EkHVrKuoUxaFXmXUfHOxlcynH2tbUSMBVTW9nZwEzQh8Rmf-p5UuNStmilfqIrLGPz8LQx5_-LBbgusQK6pjbsesCwicsM6KN-jA1E45iqufe1OfebEYzyfEGRVnFwNlCNWuGR5PY0263W-vo-tupzR0UHmjT8PD73WE-UjprTm_gPpfu9ZjCG82jdalrbmZv-d72pEd5YaBW9BSrtw2FvaFHM0IZXfIsP79MjNmXPay68pmlMiSV8bimVzgEBlmek3rC6gLGmNkURN0OQrWWCcoW8g6EMfJ3NcjUVPKi3OajdH5w',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0',
        'Accept:': 'application/json, text/plain, */*'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            answer_row = await resp.json()
            await session.close()
    return BeautifulSoup(answer_row['content'], 'html.parser')


async def answerparse(taskHash):
    x = 0
    results = []
    # ---- получение uuid заданий в тесте ----#
    
    # ---- тут получаем html в json ----#
    allsteps = await get_room(taskHash)
    random = False # проверка на рандомные задания
    for uuid in allsteps:
        print(uuid)
        x = x + 1
        soup = await get_json_html(uuid)
        try:
            anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-instruction').text.replace('\n', ' ')).replace('\r',' ')
            results.append(anstitlerow)
        except:
            try:
                anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-content-section-title').text.replace('\n', ' ')).replace('\r',' ')
                results.append(anstitlerow)
            except:
                try:
                    anstitlerow = f'№{x}📝Вопрос: ' + (soup.find('vim-text').text.replace('\n', ' ')).replace('\r',' ')
                    results.append(anstitlerow)
                except:
                    anstitlerow = f'№{x}📝Вопрос'
                    results.append(anstitlerow)
        # а тут много циклов,каждый цикл это разные типы заданий,знаю стремно,но мне лень переделывать
        if random:
            results.append('Это задание рандомное! Ответы могут не совпадать!')
        for i in soup.find_all('vim-test-item', attrs={'correct': 'true'}):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-order-sentence-verify-item'):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-input-answers'):            
            j = i.find('vim-input-item')
            results.append(await ochistka(j.text))
        for i in soup.find_all('vim-select-item', attrs={'correct': 'true'}):
            results.append(await ochistka(i.text))
        for i in soup.find_all('vim-test-image-item', attrs={'correct': 'true'}):
            results.append(f'{i.text} - Верный')
        for i in soup.find_all('math-input'):
            j = i.find('math-input-answer')
            results.append(await ochistka(j.text))
        for i in soup.find_all('vim-dnd-text-drop'):
            for f in soup.find_all('vim-dnd-text-drag'):
                if i['drag-ids'] == f['answer-id']:
                    results.append(f'{await ochistka(f.text)}')
        for i in soup.find_all('vim-dnd-group-drag'):
            for f in soup.find_all('vim-dnd-group-item'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{await ochistka(f.text)} - {await ochistka(i.text)}')
        for i in soup.find_all('vim-groups-row'):
            for l in i.find_all('vim-groups-item'):
                try:
                    a = base64.b64decode(l['text']) 
                    results.append(f"{await ochistka(a.decode('utf-8'))}")   
                except:
                    pass
        for i in soup.find_all('vim-strike-out-item', attrs={'striked': 'true'}):
            results.append(i.text)
        for i in soup.find_all('vim-dnd-image-set-drag'):
            for f in soup.find_all('vim-dnd-image-set-drop'):
                if i['answer-id'] in f['drag-ids']:
                    image = await ochistka(f['image'])
                    text = await ochistka(i.text)
                    results.append(f'{image} - {text}')
        for i in soup.find_all('vim-dnd-image-drag'):
            for f in soup.find_all('vim-dnd-image-drop'):
                if i['answer-id'] in f['drag-ids']:
                    results.append(f'{f.text} - {i.text}')
    
    return results

async def ochistka(string):
    string = string.replace('\n', '')
    string = '→ ' + string
    fraction = re.compile("dfrac{(.*?)}{(.*?)}")
    square_root = re.compile("sqrt{(.*?)}")
    power = re.compile("(.*?)\^(.*)")
    bol = re.compile("gt")
    men = re.compile("lt")
    pm = re.compile('pm')
    perp = re.compile('perp')
    menrav = re.compile('le')
    bolrav = re.compile('ge')
    syst = re.compile('begin{cases}')
    systend = re.compile('end{cases}')
    him = re.compile('mathrm{(.*?)}')
    dot = re.compile('cdot')
    strel = re.compile('rarr')
    pi = re.compile('pi')
    besk = re.compile('infty')
    for i in him.findall(string):
        string = string.replace("\mathrm{" + str(i) + "}", str(i))
    for i in fraction.findall(string):
        string = string.replace("\dfrac{" + str(i[0]) + "}{" + str(i[1]) + "}", str(i[0]) + "/" + str(i[1]))

    for i in square_root.findall(string):
        string = string.replace("\sqrt{" + str(i) + "}", "корень из " + str(i))

    for i in power.findall(string):
        string = string.replace(str(i[0]) + "^" + str(i[1]), str(i[0]) + " ^ " + str(i[1]))

    for i in bol.findall(string):
        string = string.replace("\gt", ">")
    for i in men.findall(string):
        string = string.replace("\lt", "<")
    for i in pm.findall(string):
        string = string.replace("\pm", "±")
    for i in perp.findall(string):
        string = string.replace("\perp", "⊥")
    for i in menrav.findall(string):
        string = string.replace("\le", "≤")
    for i in bolrav.findall(string):
        string = string.replace("\ge", "≥")
    for i in syst.findall(string):
        string = string.replace(r"\begin{cases}", "{")
    for i in systend.findall(string):
        string = string.replace("\end{cases}", "}")
    for i in dot.findall(string):
        string = string.replace(r"\cdot", " ⋅")
    for i in strel.findall(string):
        string = string.replace(r"\rarr", " →")
    for i in pi.findall(string):
        string = string.replace(r"\pi", "π")
    for i in besk.findall(string):
        string = string.replace(r"\infty", "∞")
    return string


