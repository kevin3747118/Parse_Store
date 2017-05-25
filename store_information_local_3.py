#-*- coding: utf-8 -*-
from DB_CONNECTION import connection
from bs4 import BeautifulSoup
import urllib.request, random, time, logging


class scrapy_need():

    def __init__(self):

        self.__az = connection.db('AZURE')
        __FORMAT = '%(asctime)s %(message)s'
        logging.basicConfig(format=__FORMAT, level=logging.INFO, filename='store.log')
        # logging.basicConfig(format=__FORMAT, level=logging.DEBUG)
        self.logger = logging.getLogger('SINGLE_STORE')

    def get_page(self, url, parameters=None):
        if parameters:
            encode_parameters = urllib.parse.urlencode(parameters).encode('utf-8')
        else:
            encode_parameters = None
        time.sleep(0.33)
        request = urllib.request.Request(url)

        ####隨機header挑選####
        foo = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36',
            'Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2722.0 Safari/537.36'
            'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
        ]
        headers = str(random.choice(foo))
        ####隨機header挑選####

        request.add_header('User-Agent', headers)
        time.sleep(0.42)
        response = urllib.request.urlopen(request, data=encode_parameters, timeout=180)
        html = BeautifulSoup(response.read().decode('utf-8'), 'lxml')
        response.close()

        return html

    def parse_store(self, store_data):

        # self.logger.info(store_data)
        # def address_remove(store_addr):
        #     result = [i for i in store_addr if not i.isdigit() and i not in '巷號弄樓之-ABC與()']
        #     address_remove_string = ''.join(result)
        #     # logging.debug(address_remove_string)
        #     return address_remove_string

        def return_store_html(store_data):

            if len(store_data) == 6:
                #特約商店名稱, 地址, 縣市名稱, 地區名稱
                terms1 = urllib.parse.quote(store_data[1] + ' ' + store_data[2])
                terms2 = urllib.parse.quote(store_data[1] + ' ' + store_data[3] + ' ' + store_data[5])
            else:
                #特約商店名稱, 分店名稱, 地址, 縣市名稱, 地區名稱
                terms1 = urllib.parse.quote(store_data[1] + ' ' + store_data[3] + ' ' + store_data[4])
                terms2 = urllib.parse.quote(store_data[1] + ' ' + store_data[3] + ' ' + store_data[2])

            url1 = 'https://www.google.com.tw/search?&q=' + terms1 + '&oq=' + terms1
            url2 = 'https://www.google.com.tw/search?&q=' + terms2 + '&oq=' + terms2

            soup1 = self.get_page(url1)
            soup2 = self.get_page(url2)

            # return url1, url2
            return soup1, soup2

        ###kernel of program###
        def verify_store_info(store_data):

            self.logger.debug(store_data)
            store_data = [i.replace('電話：', '') for i in store_data]
            if len(store_data) == 5:
                if store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[1]) > 8:
                    address = store_data[0]
                    phone = store_data[1].replace(' ', '-')
                elif store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[2]) > 8:
                    address = store_data[0]
                    phone = store_data[2].replace(' ', '-')
                elif store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[3]) > 8:
                    address = store_data[0]
                    phone = store_data[3].replace(' ', '-')
                elif store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[4]) > 8:
                    address = store_data[0]
                    phone = store_data[4].replace(' ', '-')
                elif store_data[0][0] != '0' and (sum(i.isdigit() for i in store_data[1]) < 8 or
                                                  sum(i.isdigit() for i in store_data[2]) < 8 or
                                                  sum(i.isdigit() for i in store_data[3]) < 8 or
                                                  sum(i.isdigit() for i in store_data[4]) < 8):
                    address = store_data[0]
                    phone = ''
                else:
                    address = ''
                    phone = ''
            elif len(store_data) == 4:
                if store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[1]) > 8:
                    address = store_data[0]
                    phone = store_data[1].replace(' ', '-')
                elif store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[2]) > 8:
                    address = store_data[0]
                    phone = store_data[2].replace(' ', '-')
                elif store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[3]) > 8:
                    address = store_data[0]
                    phone = store_data[3].replace(' ', '-')
                elif store_data[0][0] != '0' and (sum(i.isdigit() for i in store_data[1]) < 8 or
                                                  sum(i.isdigit() for i in store_data[2]) < 8 or
                                                  sum(i.isdigit() for i in store_data[3]) < 8):
                    address = store_data[0]
                    phone = ''
                else:
                    address = ''
                    phone = ''
            elif len(store_data) == 3:
                if store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[1]) > 8:
                    address = store_data[0]
                    phone = store_data[1].replace(' ', '-')
                elif store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[2]) > 8:
                    address = store_data[0]
                    phone = store_data[2].replace(' ', '-')
                elif store_data[0][0] != '0' and (sum(i.isdigit() for i in store_data[2]) < 8 and
                                                          sum(i.isdigit() for i in store_data[1]) < 8):
                    address = store_data[0]
                    phone = ''
                else:
                    address = ''
                    phone = ''
            elif len(store_data) == 2:
                if store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[1]) > 8:
                    address = store_data[0]
                    phone = store_data[1].replace(' ', '-')
                elif store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[1]) < 8:
                    address = store_data[0]
                    phone = ''
                else:
                    address = ''
                    phone = ''
            elif len(store_data) == 1:
                if store_data[0][0] != '0' and sum(i.isdigit() for i in store_data[0]) < 8:
                    address = store_data[0]
                    phone = ''
                elif sum(i.isdigit() for i in store_data[0]) > 8:
                    address = ''
                    phone = store_data[0].replace(' ', '-')
                else:
                    address = ''
                    phone = ''
            else:
                address = ''
                phone = ''

            # self.logger.debug((phone, address))
            return [phone, address]
        ###kernel of program###

        def verify_parking(store_data):
            parking_logo = '🚧'
            if store_data[1].find(parking_logo) == -1:
                store_data.append('不提供')
            else:
                store_data[1] = store_data[1].replace('🚧 附免費停車場', '')
                store_data.append('提供')

            return store_data

        def info(store_data):
            if len(store_data) == 6:
            # if len(store_data) == 6:
                self.logger.info('start parsing multiple stores...')
                # self.logger.debug(('info : 6', store_data))
            else:
                self.logger.info('start parsing single stores...')
                # self.logger.debug(('info : else', store_data))

        start_time = time.strftime("%Y%m%d %H:%M", time.gmtime())
        self.logger.info(start_time)
        info(store_data)

        count = 0
        for i in store_data:
#            self.logger.info(i)

            count += 1
            if count % 1200 == 0:
                time.sleep(120)

            html_result = return_store_html(i)
            html_result1 = html_result[0]
            html_result2 = html_result[1]

            store_infos = list()
            week_infos_dict = dict()
            PSD_NUM = i[0]
            date = time.strftime("%Y%m%d", time.gmtime())
            weeks = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

            ###html_result1###
            if html_result1.find_all('span', class_="_Xbe"):
                ###get address & phone###
                for store_information in html_result1.find_all('span', {'class': '_Xbe'}):
                    store_infos.append(store_information.text)

                try:
                    db_store_infos = verify_store_info(store_infos)
                except Exception as err:
                    self.logger.critical((err, i))
                ###get address & phone###

                ###get store status###
                if html_result1.find_all('span', class_="_Gtg"):
                    for status_tag in html_result1.find_all('span', class_="_Gtg"):
                        db_store_infos.append(status_tag.find_next('span').text)
                else:
                    db_store_infos.append('正常營業')
                ###get store status###

                ###provide parking place####
                db_store_infos = verify_parking(db_store_infos)
                ###provide parking place####

                ###critical message###
                if len(db_store_infos) != 4:
                    self.logger.critical(('160',i))
                ###critical message###

                ###get store open time###
                if html_result1.find_all('td', class_="_X0c"):
                    for week_tag in html_result1.find_all('td', class_="_X0c"):
                        if len(week_tag.text) != 3:
                            week_infos_dict[week_tag.text[:3]] = week_tag.find_next('td').text.replace('營業時間可能不同', '')
                        else:
                            week_infos_dict[week_tag.text] = week_tag.find_next('td').text.replace('營業時間可能不同', '')
                else:
                    for week_tag in weeks:
                        week_infos_dict[week_tag] = ''
                ###get store open time###

                ###convert db_store_infos and week_infos_dict to tuple###
                result = tuple(db_store_infos + [week_infos_dict['星期一'], week_infos_dict['星期二'],
                                                 week_infos_dict['星期三'], week_infos_dict['星期四'],
                                                 week_infos_dict['星期五'], week_infos_dict['星期六'],
                                                 week_infos_dict['星期日'], date, PSD_NUM])
                ###convert db_store_infos and week_infos_dict to tuple###
                sql_stat = ("""UPDATE [dbo].[store_information_local_3]
                                SET [google電話] = %s,[google地址] = %s,[營業狀態] = %s,[停車場] = %s
                                ,[營業時間星期一] = %s,[營業時間星期二] = %s,[營業時間星期三] = %s,[營業時間星期四] = %s
                                ,[營業時間星期五] =%s,[營業時間星期六] = %s,[營業時間星期日] = %s, [更新日期] = %s
                                WHERE [IT編號] = %s""")

                if len(result) != 13:
                    self.logger.critical(result)
                try:
                    # self.logger.debug(result)
                    self._scrapy_need__az.do_query(sql_stat, result)
                    self._scrapy_need__az.do_commit()
                # except self._scrapy_need__az.error_handle().DatabaseError as err:
                except Exception as err:
                    self.logger.critical((err, result))

            ###html_result1###

            ###html_result2###
            elif html_result2.find_all('span', class_="_Xbe"):
                ###get address & phone###
                for store_information in html_result2.find_all('span', {'class': '_Xbe'}):
                    store_infos.append(store_information.text)

                try:
                    db_store_infos = verify_store_info(store_infos)
                except Exception as err:
                    self.logger.critical((err, i))
                ###get address & phone###

                ###get store status###
                if html_result2.find_all('span', class_="_Gtg"):
                    for status_tag in html_result2.find_all('span', class_="_Gtg"):
                        db_store_infos.append(status_tag.find_next('span').text)
                else:
                    db_store_infos.append('正常營業')
                ###get store status###

                ###provide parking place####
                db_store_infos = verify_parking(db_store_infos)
                self.logger.debug(db_store_infos)
                ###provide parking place####

                ###critical message###
                if len(db_store_infos) != 4:
                    self.logger.critical(i)
                ###critical message###

                ###get store open time###
                if html_result2.find_all('td', class_="_X0c"):
                    for week_tag in html_result2.find_all('td', class_="_X0c"):
                        if len(week_tag.text) != 3:
                            week_infos_dict[week_tag.text[:3]] = week_tag.find_next('td').text.replace('營業時間可能不同', '')
                        else:
                            week_infos_dict[week_tag.text] = week_tag.find_next('td').text.replace('營業時間可能不同', '')
                else:
                    for week_tag in weeks:
                        week_infos_dict[week_tag] = ''
                ###get store open time###

                # logging.debug(week_infos_dict)

                ###convert db_store_infos and week_infos_dict to tuple###
                result = tuple(db_store_infos + [week_infos_dict['星期一'], week_infos_dict['星期二'],
                                                 week_infos_dict['星期三'], week_infos_dict['星期四'],
                                                 week_infos_dict['星期五'], week_infos_dict['星期六'],
                                                 week_infos_dict['星期日'], date, PSD_NUM])
                ###convert db_store_infos and week_infos_dict to tuple###

                sql_stat = ("""UPDATE [dbo].[store_information_local_3]
                                SET [google電話] = %s,[google地址] = %s,[營業狀態] = %s,[停車場] = %s
                                ,[營業時間星期一] = %s,[營業時間星期二] = %s,[營業時間星期三] = %s,[營業時間星期四] = %s
                                ,[營業時間星期五] =%s,[營業時間星期六] = %s,[營業時間星期日] = %s, [更新日期] = %s
                                WHERE [IT編號] = %s""")
                # self.logger.debug(result)
                if len(result) != 13:
                    self.logger.critical(result)
                try:
                    # self.logger.debug(result)
                    self._scrapy_need__az.do_query(sql_stat, result)
                    self._scrapy_need__az.do_commit()
                # except self._scrapy_need__az.error_handle().DatabaseError as err:
                except Exception as err:
                    self.logger.critical((err, result))

            else:
                result = (date, PSD_NUM)
                sql_stat = ("""update [dbo].[store_information_local_3]
                                set google電話 = '查無google資料', [google地址] = '查無google資料'
                                ,營業狀態 = '', 停車場 = '', 營業時間星期一 = '', 營業時間星期二 = ''
                                ,營業時間星期三 = '', 營業時間星期四 = '', 營業時間星期五 = ''
                                ,營業時間星期六 = '', 營業時間星期日 = '', [更新日期] = %s
                                where [IT編號] = %s""")
                try:
                    self._scrapy_need__az.do_query(sql_stat, result)
                    self._scrapy_need__az.do_commit()
                except Exception as err:
                    self.logger.critical((err, i))

        end_time = time.strftime("%Y%m%d %H:%M", time.gmtime())
        self.logger.info(end_time)

class get_store_data(scrapy_need):

    def __init__(self):
        scrapy_need.__init__(self)

    def __get_store_area(self):

        sql_stat = ("""select distinct(區) from [dbo].[store_information_local_3]
                        where google電話 is null""")
        result = self._scrapy_need__az.do_query(sql_stat)

        return result

    def get_single_store(self):

        result = list()
        __single_area = self.__get_store_area()
        # self.logger.debug(__single_area)
        for i in range(len(__single_area)):
            __single_area_parameter = str(__single_area[i][0])
            # self.logger.debug(__single_area_parameter)
            sql_stat = ("""SELECT IT編號, 店名, [地址(不含市區)], 市, 區
                           from dbo.store_information_local_3
                           where 店名 in (select 店名 FROM dbo.store_information_local_3
                           group by 店名 having count(*) <= 1 )
                           and 區 = %s and 分店 = '' and google電話 is null""")
            data = self._scrapy_need__az.do_query(sql_stat, __single_area_parameter)
            result.extend(data)
        # self.logger.debug(result)
        return result

    def __get_store_area_multi(self):

        sql_stat = ("""select distinct(區) from [dbo].[store_information_local_3]
                       where google電話 is null or google電話 = '查無google資料' """)
        result = self._scrapy_need__az.do_query(sql_stat)

        return result

    def get_multiple_store(self):

        result = list()
        __multiple_area = self.__get_store_area_multi()
        # self.logger.debug(__multiple_area)
        for i in range(len(__multiple_area)):
            __multiple_area_parameter = str(__multiple_area[i][0])
            sql_stat = ("""SELECT IT編號, 店名, 分店, [地址(不含市區)], 市, 區
                           from dbo.store_information_local_3
                           where 區 = %s and google電話 is null """)
            data = self._scrapy_need__az.do_query(sql_stat, __multiple_area_parameter)
            result.extend(data)
        # self.logger.debug(result)
        return result



if __name__ == '__main__':

    # test_data = [(123, '北投亞太溫泉生活館', '溫泉路銀光巷21-2號', '台北市', '北投區'),
    #              (456, '好日子咖啡 MD_cafe', '立農街二段293號', '台北市', '北投區')]
    stores = get_store_data()
    single_data = stores.get_single_store()
    stores.parse_store(single_data)
    multi_data = stores.get_multiple_store()
    stores.parse_store(multi_data)
    print('finish')
    ###verify area###
    # for i in data:
    #     logging.debug((i[0][5],len(i)))
    ###verify area###w
