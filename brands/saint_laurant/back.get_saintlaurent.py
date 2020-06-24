#-*- coding: utf-8 -*-
# --------------------------------------------------------------
# Get Lowest Price Data of "SAINT LAURENT" Site
# ---------------------------------------------------------------------------------------------
# By ykh  2019. 5. 3.
#         2019. 10. 31. Change Codes for Simulated "HEADLESS MODE" of Chrome (with Xvgb module)
#                                    for Processing Multi-Page Rival Prices Lists
#         2019. 11. 12. Modified Codes for accessing "FarFetch" Site and Get Data From it
#         2019. 11. 14. Add Modules for accessing the pages for each product
#         2019. 12. 13. Modified Codes for accessing "MYTHEREA" Site and Get Data From it
#         2020. 05. 26. Modified Codes for accessing "PRADA" Site and Get Data From it
#         2020. 06. 01. Modified Codes for accessing "GUCCI" Site and Get Data From it
#         2020. 06. 15. Modified Codes for accessing "CELINE" Site and Get Data From it
#         2020. 06. 15. Modified Codes for accessing "SAINT LAURENT" Site and Get Data From it
# ---------------------------------------------------------------------------------------------

import os
import sys
import csv
import glob

import time
from datetime import date
from random import randint

import requests as rq
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
# For Simulate "Headless Mode" of Chrome
from xvfbwrapper import Xvfb
from bs4 import BeautifulSoup
from lxml import html, etree

import openpyxl

sys.path.append('../../include')

from ss_sys_data import *
from lux_browser_env_setup import *

"""
from ss_rest_api_init import *
from ss_rest_api_op import *
from ss_time_api import *
from ss_rest_api_create_product import *
"""

# --------------------------------
# 가격비교 데이터 필드 인덱스 정리
# --------------------------------

match_id_idx        = 0
ad_name_idx         = match_id_idx + 1
ad_category_idx     = ad_name_idx + 1
shop_category_idx   = ad_category_idx + 1
ad_product_id_idx   = shop_category_idx + 1
post_id_idx         = ad_product_id_idx + 1
ad_product_status_idx = post_id_idx + 1
ad_import_idx       = ad_product_status_idx + 1
ad_sales_idx        = ad_import_idx + 1
ad_brands_idx       = ad_sales_idx + 1
ad_maker_idx        = ad_brands_idx + 1
sale_price_idx      = ad_maker_idx + 1
reg_date_idx        = sale_price_idx + 1
ad_price_match_name_idx = reg_date_idx + 1
ad_price_match_min_idx = ad_price_match_name_idx + 1
ad_service_status_idx = ad_price_match_min_idx + 1
ad_price_match_status_idx = ad_service_status_idx + 1
ad_price_match_id_idx = ad_price_match_status_idx + 1

"""
# -------------------------------
# New functions
# ------------------------------- """

def get_total_number(driver, portal_bags_url):

    while (True):
        print (portal_bags_url)
        driver.get(portal_bags_url)
        # print (driver.page_source)
        cookies = driver.get_cookies()
        s = requests.Session()
        for cookie in cookies:
            print (cookie)
            if (cookie['name'] == 'myth_country'):
                s.cookies.set(cookie['name'], '%7Cko-kr%7CKR')
                break
            # s.cookies.set(cookie['name'], cookie['value'])

        print ("------------------------")
        cookies = driver.get_cookies()
        for cookie in cookies:
            print (cookie)

        tree                = html.fromstring(driver.page_source)
        # total_numbers_str   = tree.xpath('//*[@id="top"]/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div/div/div[4]/div[3]/div/div[1]/p/text()')
        total_numbers_str   = tree.xpath('//div[@class="count-container"]/p/text()')
        print (total_numbers_str)

        if (len(total_numbers_str) > 0):
            break

        exit()


def get_total_page(driver, caturl):

    driver.get(caturl)
    time.sleep(6)

    tree           = html.fromstring(driver.page_source)
    total_no_pages = tree.xpath('//li[@class="last"]/a/@href')
    print (total_no_pages)

    if (len(total_no_pages) > 1):
        try:
            total_pages = int(total_no_pages[0].split('p=')[1])
            print ("TOTAL PAGES: ", total_pages)
        except:
            total_pages = 0
    else:
        total_pages = 0

    return total_pages

def get_fully_extend (driver, top_url, xpath, click_every_time=False):
   
    print ("---")
    print ("get_fully_extend")
    print ("---")

    driver.get(top_url)
    driver.implicitly_wait(15)

    time.sleep (60)

    last_height   = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    time.sleep(30)
    try:
        
        # ex_button   = driver.find_element(By.XPATH, xpath)

        """
        tree        = html.fromstring(driver.page_source)
        ex_button   = tree.xpath('//*[@id="product-listing"]/div/div[2]/div/div/a')
        """
        """
        if (ex_button != None):
            print (" Click Ex Button ")
            driver.execute_script("arguments[0].click();", ex_button)
            time.sleep(30)
        else:
            print (" No Ex Button ")
        """
        # print (" Click Ex Button ")
        # print (type(etree.tostring(ex_button)))
        # print (ex_button.page_source)
        # driver.execute_script("arguments[0].click();", ex_button)


        # ex_button.click()
        # ex_button.send_keys('\n')
        # time.sleep(30)
        # driver.execute_script("arguments[0].click();", ex_button)
        # time.sleep(30)

        while True:
            print (" SCROLL ", last_height)
            driver.execute_script ("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(10)
            driver.execute_script ("window.scrollTo(0,document.body.scrollHeight-50);")
            time.sleep(10)

            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                
                ex_button = driver.find_element(By.XPATH, xpath)
                if (ex_button != None):
                    print (" Click Ex Button ")
                    driver.execute_script("arguments[0].click();", ex_button)
                    time.sleep(30)
                else:
                    print (" No Ex Button ")

                break

            last_height = new_height

    except Exception as e:
        print (" EXCEPTION : ", e)
        # print (" NO EX BUTTON")
    
    return driver.page_source

 
def get_abstract_list(target_list):

    ret_list = []
    for aa in target_list:
        tmp = aa.replace(' ','').replace('\n','')
        if (len(tmp) > 0):
            ret_list.append(tmp)
    return ret_list



# ---------------
# Main() Function 
# ---------------

def main(test_flag=False, cat_no=1, start_index=1, end_index=200000):

    crawl_urls = [  'https://www.ysl.com/kr/saint-laurent/shop-product/%EC%97%AC%EC%84%B1/%EC%8B%A0%EC%A0%9C%ED%92%88-%ED%95%B8%EB%93%9C%EB%B0%B1',
                'https://www.ysl.com/kr/saint-laurent/shop-product/%EC%97%AC%EC%84%B1/%ED%81%AC%EB%A1%9C%EC%8A%A4%EB%B0%94%EB%94%94-%EB%B0%B1',
                'https://www.ysl.com/kr/saint-laurent/shop-product/%EC%97%AC%EC%84%B1/%EC%88%84%EB%8D%94-%EB%B0%B1',
                'https://www.ysl.com/kr/saint-laurent/shop-product/%EC%97%AC%EC%84%B1/%ED%83%91-%ED%95%B8%EB%93%A4%EB%B0%B1',
                'https://www.ysl.com/kr/saint-laurent/shop-product/%EC%97%AC%EC%84%B1/satchel-bucket-bags',
                'https://www.ysl.com/kr/saint-laurent/shop-product/%EC%97%AC%EC%84%B1/%ED%86%A0%ED%8A%B8-%EB%B0%B1',
                'https://www.ysl.com/kr/saint-laurent/shop-product/%EC%97%AC%EC%84%B1/%ED%81%B4%EB%9F%AC%EC%B9%98',
                ]
    crawl_names = [ '신상품', '크로스바디백', '숄더백', '탑핸들백', '사첼 또는 버킷백', '토트백', '클러치' ]

    cnt = 0
    if start_index < 0:
        for catname, caturl in zip(crawl_names, crawl_urls):
            cnt += 1
            print (cnt, " ) ", catname, "   ", caturl)

        return

    for catname, caturl in zip(crawl_names, crawl_urls):
        cnt += 1
        if (cnt < cat_no):
            continue

        print (" CATNAME : ", catname, "  CATURL : ", caturl)

        if (cnt == cat_no):
            submain(test_flag, catname, cnt, caturl, start_index)
        else:
            submain(test_flag, catname, cnt, caturl, 1)



            
            


# ---------------
# Submain() Function 
# ---------------

def submain(test_flag=False, catname="", catcnt=0, caturl="", start_index=1):

    # -------------
    # Open Database 
    # -------------
    
    if (test_flag == True):
        db = connect_database()
    else: 
        db = connect_database()
        # db = connect_database_with_name("luxpace_db")
    cursor = db.cursor()

    # ----------------------------------------------------------------------
    # MYTHERESA 사이트 상품 정보 URL
    # ----------------------------------------------------------------------
    portal_ap = "https://ysl.com/kr/"
    # portal_bags_url = portal_ap + caturl
    portal_bags_url = caturl
    page_str = "?p=$"

    # ------------------------------
    # Default Values
    # ------------------------------

    site_id = 100004
    """ 
                    # 100001 = PRADA, 100002 = GUCCI, 100003 = CELINE, 100004 = SAINT LAURENT
    """
    site_product_att_category = '백'
    site_product_att_subcategory = catname
    site_product_att_department = 'WOMEN'
    # usd_to_krw_ex_rate = 1200

    # ----------------------------------------------------------------------
    # 가격비교 제품 List 확보
    # ----------------------------------------------------------------------

    cnt = start_index

    # -----------------------
    # Create a Chrome Browser (in Virtual X-Window Mode / Not Visual)
    # -----------------------
    
    # browser_toggle = 'FIREFOX'
    browser_toggle = 'CHROME'
    driver, v_display = set_browser_ready_for_crawling(test_flag, browser_toggle)

    try:

        print ("----------------------------")
        print ("Start to Crawl SAINT LAURENT")
        print ("----------------------------")
        print (" SUBCAT: ", catname, " [ ", catcnt, " ] ", caturl)
        curr_page = 0 
        total_cnt = 0
        total_pages = 0
        image_case = 0

        top_url = portal_bags_url

        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5];},});")
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        driver.execute_script("const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};")



        """                                               /html/body/div[1]/main/div[1]/div[5]/div/div[2]/button """
        """                                               /html/body/div[1]/main/div[1]/div[5]/div/div[2]/button """
        # page_source = get_fully_extend (driver, top_url, '//*[@id="searchresults"]/div[5]/div/div[2]/button', True)  # True = Click Every Scroll
        page_source = get_fully_extend (driver, top_url, '/html/body/div[1]/main/div[1]/div[5]/div/div[2]/button', True)  # True = Click Every Scroll
                                                                                                                     # False = Click Only First

        tree = html.fromstring(page_source)
        prds = tree.xpath('//*[@id="searchresults"]/div[5]/div/div[1]/article')
        time.sleep(6)

        if (len(prds) <= 0):
            print (" There is no products in SUBCAT : ", catname)
            return

        print (" Number of products in this page : ", len(prds))

        cnt = 0

        product_currency  = 'KRW'
        product_designer  = 'SAINT LAURENT'

        prd_id_str      = './/article/@data-ytos-item'
        prd_base_str    = './/article/@data-ytos-track-product-data'

        # price_str       = './/article/'
        product_hrefs_str = './/article/a/@href'
        product_name_str  = './/article/a/@aria-label'
        product_image_str = './/article/a/div/img[1]/@data-origin  \
                            |.//article/a/div/img[2]/@src \
                            |.//article/a/div/img[3]/@data-origin'
        
        print ("=== Total Products of this SUBCAT : ", len(prds))

        for pb in prds:
            cnt += 1

            if (cnt < start_index):
                continue

            print (" >>> ", pb)
            prd_id_list         = pb.xpath(prd_id_str)
            if (len(prd_id_list) == 0):     # Skip the dummy items
                cnt -= 1
                continue
            prd_id = prd_id_list[0]
            print (prd_id)

            prd_brand_code_list = prd_id
            prd_base            = prd_base_str

            print ("--")
            meta_json = json.loads(pb.xpath(prd_base_str)[0])
            print ("*****")
            for aa in meta_json:
                print (aa, meta_json[aa])

            print ("----")

            # continue

            """
            print (prd_id_list, prd_id)
            print (prd_brand_code_list)
            print (prd_base)
            """

            price = meta_json['price']
            ref_price = meta_json['basePrice']
            product_names = meta_json['name']
            color = meta_json['color']
            size  = meta_json['size']

            print (price, ref_price)
            print (product_names)


            product_hrefs     = pb.xpath(product_hrefs_str.replace('$',prd_id))
            # product_names     = pb.xpath(product_name_str.replace('$',prd_id))
            product_images    = pb.xpath(product_image_str.replace('$',prd_id))

            site_product_code = prd_id 

            # prd_brand_code    = prd_brand_code_list[0]
            prd_brand_code    = prd_id
            

            print ("       ")
            print (" ==========================================")
            print (" SUBCAT : ", catname, " [ ", catcnt, " ] ", caturl)
            print (" CNT : ", cnt)
            print (product_hrefs)
            print (product_currency)
            print (product_designer)
            print (product_names)
            print (price)
            print (site_product_code)
            print (prd_brand_code)
            print (" No of images : ", len(product_images))

            product_images_list = []
            for aa in product_images:
                temp_url = aa.split('?sw=300')[0]
                product_images_list.append(temp_url)
            # print (etree.tostring(product_images[0]))

            print (" === --- === ")
            # product_images_list = get_unparserable_tags(product_images, 'src=', ["//media.gucci.com/", "470x470",".jpg"])

            # Show the list of Pictures
            for aa in product_images_list:
                print(aa)

            # CHECK THE SAME ITEM IS ALREADY REGISTERED IN DB
            # IF THERE IS, SKIP IT. IF NOT, PROCESS IT BY FETCHING THE PRODUCT PAGE

            txt = input(" Next Page ? ")
            if (txt == 'q' or txt == 'Q'):
                exit()
            continue


            if (test_flag == True):
                ret = []
            else:
                cursor.execute("SELECT site_product_idx FROM brand_site_product \
                                   WHERE  site_id=%s and site_product_code=%s", \
                                  (site_id, prd_brand_code))
                ret = cursor.fetchall()

            # continue

            if (len(ret) == 0 or ret[0][0] == 0):       # If there is a matched field, skip it
            # if (True):
                product_url = portal_ap + product_hrefs[0]
                print (product_url)
                driver.get(product_url)
                time.sleep(3)
                
                org_regular_price = org_sale_price = org_discount_rate = 0

               # desc, color, material, country, desc, measure, prd_imgs \
                desc, color, d_material, d_country, desc, measure, image_urls, d_brand_code, \
                d_krw_regular_price, d_krw_sale_price, d_krw_discount_rate    \
                      = get_product_info_from_each_product_page(driver, driver.page_source, product_images_list)

                print (d_brand_code)
                print (color)
                print (measure)

                print ("Site code: ", prd_brand_code)

                print (desc)
                # print (color)
                # print (material)
                # print (country)
                print (measure)
                print (" --- ")
                for qq in image_urls:
                    print (qq)
                print (" --- ")
                print (d_brand_code)
                # print (krw_regular_price)
                # print (krw_sale_price)
                # print (krw_discount_rate)

                """
                txt = input(" Next Page ? ")
                if (txt == 'q' or txt == 'Q'):
                    exit()
                """ 

                # continue # Enable to register into DB """

                cursor.execute("SELECT site_product_idx FROM brand_site_product \
                            WHERE  site_id=%s and site_product_code=%s", \
                            (site_id, prd_brand_code))
                ret = cursor.fetchall()
                print ("check luxpace_db")
                print (ret)

                    # material = measure = color = country = ''

                if (len(ret) == 0 or ret[0][0] == 0):   # If there is a matched field, skip it
                    cursor.execute("INSERT INTO brand_site_product \
                                    (site_id, site_product_code, site_product_url, \
                                     site_brand_product_code, site_brand, \
                                     site_product_name, site_product_description, \
                                     site_product_att_category, \
                                     site_product_att_subcategory, site_product_att_material, \
                                     site_product_att_measure, site_product_att_color, \
                                     site_product_att_madein, site_product_att_department, \
                                     site_original_currency, site_original_regular_price, \
                                     site_original_sale_price, site_original_discount_rate, \
                                     site_krw_regular_price, site_krw_sale_price, \
                                     site_krw_discount_rate) \
                                VALUES (%s,%s,%s,  %s,%s,  %s,%s,%s,  %s,%s,  %s,%s, \
                                        %s,%s,     %s,%s,  %s,%s,  %s,%s,  %s)", \
                                (site_id, prd_brand_code, product_url, \
                                 '', product_designer, \
                                 product_names[0], desc, site_product_att_category, \
                                 site_product_att_subcategory, d_material, \
                                 measure, color, \
                                 d_country, site_product_att_department, \
                                 product_currency, org_regular_price, \
                                 org_sale_price, org_discount_rate, \
                                 d_krw_regular_price, d_krw_sale_price,\
                                 d_krw_discount_rate))
                    cursor.execute("SELECT site_product_idx FROM brand_site_product \
                                 WHERE  site_id=%s and site_product_code=%s", \
                               (site_id, prd_brand_code))
                    ret = cursor.fetchall()
                    print (ret)
                    if (len(ret) > 0 and ret[0][0] > 0):
                        site_product_idx = ret[0][0]
                    else:
                       print ("ERROR TO GET 'site_product_idx'")
                       continue
              
                else:
                    site_product_idx = ret[0]

                print (" ")
                print ("  GET site_product_idx", site_product_idx)
                print (" ")

                for tt in image_urls:
                    print ("Register Image URLs : ", tt)
                    cursor.execute ("INSERT INTO org_image \
                                   (site_id, site_product_idx, site_image_url) \
                                   VALUES (%s, %s, %s)",
                                   (site_id, site_product_idx, tt))

            else:
                continue


            """
            print ("GET INFO FROM EACH PAGE : ", product_hrefs)
            # driver.get(product_hrefs[0])

            # desc, color, material, country, desc, measure, prd_imgs \
            desc, color, material, country, desc, measure, image_urls, site_product_code, \
                  regular_price, sale_price, discount_rate    \
                        = get_product_info_from_each_product_page(driver.page_source)             
            
            """

            # exit()
            continue

    finally:
        close_browser_for_crawling (test_flag, driver, v_display)


def get_unparserable_tags (elem_list, spliter=['srcset="'], keys=['https:', '800.1000.jpg'], masks=['-src_small']):

    print (" --------------------- ")
    print (" get_unparserable_tags ")
    print (" --------------------- ")

    rst_list = []

    for elem in elem_list:

       img_raw_str = str(etree.tostring(elem))
       # print (":::")
       # print (img_raw_str)
       img_list_str = []
       temp_img_strs = img_raw_str.split(spliter)

       for aa in temp_img_strs:

           skip_flag = False
           for mm in keys:
               if (mm not in aa):
                   skip_flag = True
                   break
           if skip_flag == True:
               continue
           
           for mm in masks:
               if (mm in aa):
                   skip_flag = True
                   break
           if skip_flag == True:
               continue

           temp_str = aa.replace(',',' ').replace('<', '').replace('>','').replace('"','').replace('/\n','').split(' ')
           # print (" --")
           # print (" ")
           # print (" aa : ", temp_str)
           for bb in temp_str:
               # print (" ")
               # print (" bb: ", bb, ('https:' in bb), ('800.1000.jpg' in bb))
               key_avail_flag = True
               for xx in keys:
                   if xx not in bb:
                       key_avail_flag = False
                       break
               if (key_avail_flag == True):

                   for cc in bb.split(' '):
                       # print (" ")
                       # print (" cc : ", cc)
                       if (cc in img_list_str) or (cc in rst_list):
                           continue

                       key_avail_flag2 = True
                       for yy in keys:
                           if yy not in cc:
                               key_avail_flag2 = False
                               break

                       if (key_avail_flag2 == True):
                           # print ('>>> ',img_list_str)
                           img_list_str.append(cc)
                           # print ('                  >>> + ',img_list_str)

       if (len(img_list_str) > 0):
           for aa in img_list_str:
               if ('https:' not in aa):
                rst_list.append('https:' + aa)
       rst_list.sort()

    return rst_list


def find_max_matches (driver, tree, xpath):

    print ("----------------")
    print ("find_max_matches")
    print ("----------------")
    
    if ('//' not in xpath):
        return ""
    xpath_list = xpath.split("/")
    if (len(xpath_list) == 0):
        return ""

    prev_xpath = ""
    curr_xpath = "/"

    print ("xpath_list: ", xpath_list)

    for aa in xpath_list:
        if aa == "":
            continue
        prev_xpath = curr_xpath
        curr_xpath = curr_xpath + "/" + aa
        # print (" Curr xpath: ", curr_xpath)
        curr_elems = tree.xpath(curr_xpath)
        # print (" Curr Elems: ", curr_elems)
        if (len(curr_elems) <= 0):
            break
    print (" : ", prev_xpath)

    return prev_xpath





def get_product_info_from_each_product_page(driver, prd, images):

    print ("--- ---")
    print (" get_product_info_from_each_product_page ")
    print ("--- ---")

    # print (prd)

    tree = html.fromstring(prd)

    # curr_xpath = find_max_matches(driver, tree, '//*[@id="page"]/div[3]/div/div[1]/div[4]/div[1]/section/div/div/div/div/div/picture')
    curr_xpath = '//*[@id="product-details-main"]/main/div[2]/section/div[2]/div/ul/li/button/img/@src'


    """     //*[@id="page"]/div[3]/div/div[1]/div[4]/div[1]/section/div/div/div/div/div[1]/picture  """
    """     //*[@id="page"]/div[3]/div/div[1]/div[4]/div[1]/section/div/div/div/div/div[2]/picture  """
    #       //div[@aria-live="polite"] \
    """
    image_urls  = tree.xpath('          \
            //*[@class="slick-track"] \
            ')
    """


    image_urls  = tree.xpath(curr_xpath)

    print (" --------------------- ")
    print (" RETURNED CURR_XPATH : ", curr_xpath)
    print (" --------------------- ")
    print (len(image_urls), image_urls)


    """
    # img_raw_str = get_unparserable_tags(image_urls, 'src=', ["//media.gucci.com/", "470x470", ".jpg"])
    # img_raw_str2 = get_unparserable_tags(image_urls, 'src=', ["//media.gucci.com/", "490x490", ".jpg"])
    images  = get_unparserable_tags(image_urls, 'srcset=', ["//media.gucci.com/", "470x470", ".jpg"], ["-src_small"])
    images2 = get_unparserable_tags(image_urls, 'srcset=', ["//media.gucci.com/", "490x490", ".jpg"], ["-src_small"])

    if (len(images2) > len(images)):
        images = images2

    img_raw_str = []

    for xx in images:
        if xx not in img_raw_str:
            img_raw_str.append(xx)


    # print (img_list_str)
    print (" === --- === ")
    for aa in img_raw_str:
        print (aa)
    """
    
    # image_urls = img_raw_str
    # image_urls = list(set(image_urls))
    # print (image_urls)

    # site_product_code   = tree.xpath('//*[@id="product-details"]/div[1]/span/text()')
    product_brand       = "CELINE"
    # product_name        = tree.xpath('//*[@id="product-detail-add-to-shopping-bag-form"]/div/div[1]/h1/text()')
    # product_price       = tree.xpath('//*[@id="markedDown_full_Price"]/text()')
    # product_old_price   = 
    # product_new_price   = tree.xpath('//p[@class="special-price"]/span/text()')
    # product_discount    =  0
    
    product_desc        = tree.xpath('//*[@id="product-details-main"]/main/div[2]/section/div[2]/form/p[2]/text()')

    # product_sizes       = tree.xpath('//*[@id="pdp_details"]/div/article[1]/div/div/text()')

    # desc_super_str = color = material = country = measure = image_urls = brand_code = krw_regular_price = krw_sale_price = krw_discount_rate = 0

    # print (" site_product_code : " , site_product_code) 
    # print (" product_brand : ",      product_brand)
    # print (" product_name  : ",      product_name)
    # print (" product_price : ",      product_price)
    print (" product_desc  : ",      product_desc)
    # print (" product_size  : ",      product_sizes)

    desc_super_str = color = material = measure = country = ''

    temp_size = " "
    for xx in product_desc:
        if ('CM' in xx) and ('IN' in xx) and ('x' in xx):
            temp_size += xx.replace('\n','').replace('cm', 'cm ') + " "
        if ('제조국:' in xx) or ('Made In' in xx) or ('made' in xx):
            country = xx
    print (" final size : ", temp_size)


    # brand = product_brand[0]
    # name  = product_name[0]

    color  = tree.xpath('//*[@id="ddt-productColour"]/text()')

    for aa in product_desc:
        print (" >>> ", aa) 
        desc_super_str += aa + ","
    """
    for aa in temp_size:
        measure += aa + ","
    """
    measure = temp_size

    image_list = []
    for aa in image_urls:
        image_list.append(aa.split('?sw=')[0])
    image_urls = image_list

    
    if (True):
        # price = float(product_price[0].replace(' ','').replace('￦','').replace('₩','').replace(',',''))
        # print (" price : ", price)
        price = 0
        site_prd_code = 0
        return  desc_super_str, color[0], material, country, desc_super_str, measure, image_urls, site_prd_code, \
            price, price, 0
    """
    else:
        old_price = float(product_old_price[0].replace(' ','').replace('','').replace(',',''))
        new_price = float(product_new_price[0].replace(' ','').replace('€','').replace(',',''))
        discount  = float(product_discount[0].replace(' ','').replace('%','').replace('할인',''))
        print (" prices : ", old_price, new_price, discount)
        return  desc_super_str, color, material, country, desc_super_str, measure, image_urls, site_product_code, \
            old_price, new_price, discount
    """


    print (" ========= ")
    print ("  =======  ")



# ------------------------------
# Processing Commandline Command
# ------------------------------

# print ("START TO GET LOWEST PRICES ", len(sys.argv))
# 
# Check whether it should be processed in "TEST" mode (with Visual Browsers)
#

len_argvs = len(sys.argv)
last_argv = sys.argv[len_argvs-1] 

print (len_argvs)


if 'TEST' in last_argv:
    len_argvs -= 1
    test_flag = True
else:
    test_flag = False


if len_argvs > 4 or (len_argvs >= 2 and sys.argv[1] == '?'):
    print (" ----------------------------------------------- ")
    print (" usage: {} ['?'/[si, ei] ".format(sys.argv[0]))
    print ("        si: start index of match_ids")
    print ("        ei: end index of match_ids")
    print ("        ? : help + total number of index of match_ids")
    print ("")
    total_cnt = main(test_flag, "?")
    print (" Total number of match_ids' index is : ", total_cnt)

    """
    print (" usage: {} [1/2] [start match_id] ".format(sys.argv[0]))
    print ("        If option = 1, Only For Not MIN PRICES")
    print ("           option != 1, For Not ALL PRICE MATCHES")
    print ("           DEFAULT is 1")
    """
    print (" ----------------------------------------------- ")
    # return(total_cnt)
elif len_argvs == 2:
    main(test_flag, int(sys.argv[1]))
elif len_argvs == 3:
    main(test_flag, int(sys.argv[1]), int(sys.argv[2]))
else:
    main(test_flag)
    # total_cnt = main("?")
    # print (" Total number of match_ids' index is : ", total_cnt)
    # return(total_cnt)
    # main('?')
