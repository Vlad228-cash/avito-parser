import sqlite3 as sql
import requests 
from bs4 import BeautifulSoup as bs 
import re
    
def App(cursor,model,memory,condition,price):
    cursor.execute('INSERT INTO products (model,memory,condition,price) VALUES (?,?,?,?)',(model,memory,clean_text(condition),clean_price(price)))

def clean_price(text):
    return text.replace('\xa0', '')
def clean_text(text):
    return re.sub(r'[^\w\s]', '', text)

def Requ(url):
    response = requests.get(url)
    soup = bs(response.text,'html.parser')
    div = soup.find('div',class_= 'index-root-H81wX')
    values = div.find_all('div',class_='iva-item-root-XBsVL photo-slider-slider-Yf84l iva-item-list-Jer96 iva-item-redesign-yiAjA iva-item-ivaItemRedesign-QmNXd iva-item-responsive-nSYjv items-item-UjqLI items-listItem-Qazzp js-catalog-item-enum')

    return values

def iphone(url,cursor):
    phones = Requ(url)

    for phone in phones:
        desciption = phone.find('a',class_ = 'styles-module-root-cfrVG styles-module-root_underlineOffset_size-m-ce9r8 styles-module-root_noVisited-U4swI styles-module-root_preset_black-VfJP4').get_text().split(',')
        model = desciption[0]
        memory = desciption[1]
        price = phone.find('span',class_ = 'styles-module-size_l-kPWfk styles-module-size_l_dense-kvYNM').get_text()
        condition = phone.find('p',class_ = 'styles-module-root-PY1ie styles-module-size_m-w6vzl styles-module-size_m_dense-HvBLt styles-module-size_m-DKJW6 styles-module-size_dense-u0sRJ stylesMarningNormal-module-root-OE0X2 stylesMarningNormal-module-paragraph-m-dense-mYuSK').get_text()
        App(cursor,model, memory, condition, price)

def airpods(url,cursor):
    airs = Requ(url)

    for air in airs:
        desciption = air.find('a',class_ = 'styles-module-root-cfrVG styles-module-root_underlineOffset_size-m-ce9r8 styles-module-root_noVisited-U4swI styles-module-root_preset_black-VfJP4').get_text().split(',')
        price = air.find('span',class_ = 'styles-module-size_l-kPWfk styles-module-size_l_dense-kvYNM').get_text()
        if 'AirPods Pro 2' in desciption[0]:
            App(cursor,'AirPods Pro 2', 'pass', 'Бу', price)


def macbook(url,cursor):
    macs = Requ(url)

    for mac in macs: 
        desciption = mac.find('a',class_ = 'styles-module-root-cfrVG styles-module-root_underlineOffset_size-m-ce9r8 styles-module-root_noVisited-U4swI styles-module-root_preset_black-VfJP4').get_text().split(',')
        model = ''
        memory = 'pass'
        for d in desciption[0].split():
            for x in ('gb','Gb','Tb','GB'):
                if x in d:
                    memory = d
        price = mac.find('span',class_ = 'styles-module-size_l-kPWfk styles-module-size_l_dense-kvYNM').get_text()
        App(cursor, 'MacBook Air 15', memory, 'Новый', price)

def main():
    conn = sql.connect('avito.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM products')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="products"')

    cursor.execute('''CREATE TABLE IF NOT EXISTS products 
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT,
                memory TEXT,
                condition TEXT,
                price INTEGER)
                ''')

    data_url = {
        'iphone16_pro_max' : 'https://www.avito.ru/rostov-na-donu/telefony/mobilnye_telefony/apple/iphone_16_pro_max-ASgBAgICA0SywA3MsYwVtMANzqs5sMENiPw3?cd=1&context=H4sIAAAAAAAA_0SRwXLbIBiE38XXHPJLieNaOSXIoqiYjkgiIW4WchAuslMLg9VO370jN54eYZZvdj82SZT8HpIIkpk6HI9b5cxhP3sckvvlQzIje6dIn-1abH1jg_lug1F9GRqc7WQZDM2CkaKbzqda8I8mniuy-1DEoReofTG0-AloWvgWU8LwCuiuOC3xGmrKNcOUopTrFt0AXXDt0AhUcO3wM9S0GBxOoV5w06J7oG8a6HsxMHQLdVr4S2atw08_3c2hfi28Q0uSrmJyzZi08AwFoEeu1bcFtf_6Knzu6rh0spqDQORBoNzI6uzb6HMPLn9tqvZU9uWo4v-7m345NlU20CobpMint4NA-bCp5kcVTRm3ECgfpcgiKdiFvY2CUaK0am-vXgLQPe_YtBn0-rXWQG-5ZuiGMPRlcnVy-PnKbmLWXdz_sKuJx3Zv4zp9Cu8vZ0X23G6_8it3OznzDEVA74oTwwjqsyLmrEgf2RZ3Xmaf_xeXnerZQdzlVmI7ymrqmi-FADN7_PM3AAD__y0WtX8RAgAA',
        'airpods2_pro' : 'https://www.avito.ru/rostov-na-donu/audio_i_video/naushniki-ASgBAgICAUSIAtRO?context=H4sIAAAAAAAA_0SRwXKbMBRF_4VtFnmQOK7JKhFGFZXVQUlAYmeEI0SFnRoZmXb67x3ceLrSSHN15t3ztnEU_x7iEOJAHY7HnXLmsA8eh_h-9RAHZO8U6dOuwXasrTffrTeqL3yN064qvKGpN5Vo5_tJCv5RRwtFug9FHHoBOeZDg5-AJvnYYEoYXgPt8tMKb0BSrhmmFCVcN-gG6JJrhyaggmuHn0HSfHA4AbnkpkH3QN800Pd8YOgWZJKPl8xG-5_j_LYA-ZqPDq1Iso7INWOSfGTIAz1yrb4tqf03r8LnVkaFq8oFCEQeBMpMVZ7HJvzsg4tf27I5FX0xqeh_77pfTXWZDrRMh0pk899BoGzYloujCueMWwqUTZVIw0qwC3sXeqNEYdXeXr14oHvesrkz6M2r1EBvuWbohjD0ZXZ1cvj5yq4j1l7c_7Drmce6t2mTPPn3l7Mie253X_mVu5udjQyFQO_yE8MI5FkRc1akD22D27FKP_cXFa3q2UHcZbbCdqrKedZsJQSYefFhHEyX8yEOEs1S451AMuqOoi2Cxz9_AwAA__8R4In-MQIAAA&localPriority=0&q=airpods+2+pro',
        'macbook15_air' : 'https://www.avito.ru/rostov-na-donu/noutbuki?context=H4sIAAAAAAAA_2xS3XabPBB8F14gAr44H-TKFoGIAglqDRJ3IAg_Fg4xsgTu6bv3yHZPb3rFYVYzu7OzpWu5P2fXBK7BPk-nhon-82g8z-7j5j_XQEfB0OgPdcBlxVX_xlXPxkxVgT8UmeojX_UF6fT_mRI8VdYjQ8PEkIA1iAbcOdAE0Xsqey-VNTTJ617FwYsCkZ3OSYBAJFMpgh2gqgXRQyr5YsberosTaIPIS6UTbEH0hNs68FD87VTl_kBHR5brrisJWmMPmeo0n4m_nEH4kEoBN5onHKh74H71cJvoGT5w68AnQC-4FVABGulaKhKN_d-qLyFonvSV5ZxQ4E-s3_7VhmgmMLx5zk1eHfHN4xjyKnDse_1QkGQqrMe8IOGlzB3N2xAYnis7FDRXguYLZ5rbLwyNy1SN4qLf5LZg6BhyRjLO7Kv2E4HhUufZ2mS3nf_L973vQAnmheWszZ6_aL23H63G58pKumtuhxueDPs19rbq4_vC0BHz5hX_yaoBNErldU92ek4CCOhyn9PkddDJwr9nb_uK2LVkI9Z30JVWthILT4XFAYGhQwjo9fGYrrFevxvXQOBdoqY0u5p-lQdvNJ5__Q4AAP__sRdDdnUCAAA&localPriority=0&q=macbook+air+15'
    }

    iphone(data_url['iphone16_pro_max'],cursor)
    airpods(data_url['airpods2_pro'],cursor)
    macbook(data_url['macbook15_air'],cursor)

    conn.commit()
    cursor.execute('SELECT * FROM products')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()
main()